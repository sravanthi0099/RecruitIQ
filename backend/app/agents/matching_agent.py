"""Candidate-to-job matching agent."""

from typing import Dict, Any, List
from loguru import logger

from app.agents.base_agent import BaseAgent
from app.services.matching_service import matching_service


class MatchingAgent(BaseAgent):
    """Agent for matching candidates to jobs."""

    def __init__(self):
        """Initialize Matching Agent."""
        super().__init__(name="MatchingAgent", version="1.0.0")

    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute candidate-job matching.
        
        Args:
            input_data: Must contain 'candidate_skills', 'required_skills', etc.
            
        Returns:
            Matching result
        """
        candidate_skills = input_data.get("candidate_skills", [])
        required_skills = input_data.get("required_skills", [])
        candidate_years = input_data.get("candidate_years", 0)
        min_years = input_data.get("min_years", 0)
        max_years = input_data.get("max_years", 20)

        logger.info(
            f"{self.name}: Matching candidate to job",
            extra={
                "candidate_skills": len(candidate_skills),
                "required_skills": len(required_skills),
            },
        )

        # Calculate match scores
        skill_score = matching_service.calculate_skill_match_score(
            candidate_skills,
            required_skills,
        )

        experience_score = matching_service.calculate_experience_match_score(
            candidate_years,
            min_years,
            max_years,
        )

        overall_score = matching_service.calculate_overall_match_score(
            skill_score,
            experience_score,
        )

        # Generate explanation
        explanation = self._generate_explanation(
            candidate_skills,
            required_skills,
            candidate_years,
            min_years,
            skill_score,
            experience_score,
        )

        result = {
            "match_score": round(overall_score, 3),
            "skill_score": round(skill_score, 3),
            "experience_score": round(experience_score, 3),
            "explanation": explanation,
            "strengths": self._identify_strengths(candidate_skills, required_skills),
            "gaps": self._identify_gaps(candidate_skills, required_skills),
        }

        logger.info(
            f"{self.name}: Matching complete",
            extra={"overall_score": overall_score},
        )

        return result

    def _identify_strengths(
        self,
        candidate_skills: List[str],
        required_skills: List[str],
    ) -> List[str]:
        """
        Identify candidate strengths.
        
        Args:
            candidate_skills: Candidate's skills
            required_skills: Required skills
            
        Returns:
            List of strengths
        """
        strengths = []
        candidate_skills_lower = [s.lower() for s in candidate_skills]

        for skill in required_skills:
            if skill.lower() in candidate_skills_lower:
                strengths.append(skill)

        return strengths

    def _identify_gaps(
        self,
        candidate_skills: List[str],
        required_skills: List[str],
    ) -> List[str]:
        """
        Identify skill gaps.
        
        Args:
            candidate_skills: Candidate's skills
            required_skills: Required skills
            
        Returns:
            List of missing skills
        """
        gaps = []
        candidate_skills_lower = [s.lower() for s in candidate_skills]

        for skill in required_skills:
            if skill.lower() not in candidate_skills_lower:
                gaps.append(skill)

        return gaps

    def _generate_explanation(
        self,
        candidate_skills: List[str],
        required_skills: List[str],
        candidate_years: float,
        min_years: float,
        skill_score: float,
        experience_score: float,
    ) -> Dict[str, str]:
        """
        Generate match explanation.
        
        Args:
            candidate_skills: Candidate's skills
            required_skills: Required skills
            candidate_years: Candidate's experience
            min_years: Minimum required experience
            skill_score: Skill match score
            experience_score: Experience match score
            
        Returns:
            Explanation dictionary
        """
        explanations = {}

        # Skill explanation
        matched_skills = sum(1 for s in required_skills if s.lower() in [x.lower() for x in candidate_skills])
        skill_pct = (matched_skills / len(required_skills) * 100) if required_skills else 0
        explanations["skills"] = f"Matches {matched_skills}/{len(required_skills)} required skills ({skill_pct:.0f}%)"

        # Experience explanation
        if candidate_years >= min_years:
            explanations["experience"] = f"Has {candidate_years:.0f} years (required: {min_years:.0f})"
        else:
            explanations["experience"] = f"Has {candidate_years:.0f} years (required: {min_years:.0f}, gap: {min_years - candidate_years:.0f} years)"

        return explanations