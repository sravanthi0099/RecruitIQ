"""Salary estimation and market intelligence agent."""

from typing import Dict, Any
from loguru import logger

from app.agents.base_agent import BaseAgent


class SalaryAgent(BaseAgent):
    """Agent for salary estimation and market intelligence."""

    def __init__(self):
        """Initialize Salary Agent."""
        super().__init__(name="SalaryAgent", version="1.0.0")
        self.base_salaries = {
            "junior": {"min": 50000, "max": 80000},
            "mid": {"min": 80000, "max": 130000},
            "senior": {"min": 130000, "max": 200000},
            "lead": {"min": 200000, "max": 300000},
        }

    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute salary estimation.
        
        Args:
            input_data: Job title, location, experience, skills
            
        Returns:
            Salary estimation result
        """
        job_title = input_data.get("job_title", "")
        location = input_data.get("location", "")
        experience_years = input_data.get("experience_years", 0)
        skills = input_data.get("skills", [])

        logger.info(
            f"{self.name}: Estimating salary",
            extra={
                "job_title": job_title,
                "location": location,
                "experience_years": experience_years,
            },
        )

        # Determine seniority level
        seniority = self._determine_seniority(experience_years)

        # Get base salary range
        base_range = self.base_salaries.get(seniority, self.base_salaries["mid"])

        # Apply location adjustment
        location_multiplier = self._get_location_multiplier(location)

        # Apply skill premium
        skill_multiplier = self._calculate_skill_multiplier(skills)

        # Calculate final salary
        min_salary = base_range["min"] * location_multiplier * skill_multiplier
        max_salary = base_range["max"] * location_multiplier * skill_multiplier
        avg_salary = (min_salary + max_salary) / 2

        result = {
            "estimated_salary": round(avg_salary, 0),
            "salary_range": {
                "min": round(min_salary, 0),
                "max": round(max_salary, 0),
            },
            "seniority_level": seniority,
            "location": location,
            "location_multiplier": round(location_multiplier, 2),
            "skill_multiplier": round(skill_multiplier, 2),
            "market_data": {
                "percentile_25": round(min_salary * 0.95, 0),
                "percentile_50": round(avg_salary, 0),
                "percentile_75": round(max_salary * 1.05, 0),
            },
            "currency": "USD",
        }

        logger.info(
            f"{self.name}: Estimation complete",
            extra={"estimated_salary": avg_salary},
        )

        return result

    def _determine_seniority(self, experience_years: float) -> str:
        """
        Determine seniority level based on experience.
        
        Args:
            experience_years: Years of experience
            
        Returns:
            Seniority level
        """
        if experience_years < 2:
            return "junior"
        elif experience_years < 7:
            return "mid"
        elif experience_years < 12:
            return "senior"
        else:
            return "lead"

    def _get_location_multiplier(self, location: str) -> float:
        """
        Get salary multiplier based on location.
        
        Args:
            location: Job location
            
        Returns:
            Location multiplier
        """
        location_lower = location.lower()

        # High cost of living areas
        if any(city in location_lower for city in ["san francisco", "new york", "boston", "seattle"]):
            return 1.4

        # Medium cost of living areas
        if any(city in location_lower for city in ["chicago", "denver", "austin", "philadelphia"]):
            return 1.2

        # Low cost of living areas
        if any(city in location_lower for city in ["dallas", "miami", "atlanta", "minneapolis"]):
            return 0.95

        # Remote
        if "remote" in location_lower:
            return 1.1

        return 1.0

    def _calculate_skill_multiplier(self, skills: list) -> float:
        """
        Calculate salary multiplier based on skills.
        
        Args:
            skills: List of skills
            
        Returns:
            Skill multiplier
        """
        premium_skills = ["AWS", "Kubernetes", "AI", "ML", "Rust", "Go"]
        
        premium_count = sum(1 for skill in skills if any(ps.lower() in skill.lower() for ps in premium_skills))
        
        multiplier = 1.0 + (premium_count * 0.05)
        
        return min(1.3, multiplier)  # Cap at 30% premium