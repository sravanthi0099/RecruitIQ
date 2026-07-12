from typing import Dict, Any
import re

from app.agents.base_agent import BaseAgent


class JDAgent(BaseAgent):
    """Rule-based Job Description Intelligence Agent."""

    def __init__(self):
        super().__init__(
            name="JDAgent",
            version="2.0.0"
        )

        self.skill_keywords = [
            "Python",
            "FastAPI",
            "Django",
            "Flask",
            "Java",
            "Spring Boot",
            "JavaScript",
            "TypeScript",
            "React",
            "Angular",
            "Vue",
            "Node.js",
            "PostgreSQL",
            "MySQL",
            "MongoDB",
            "Redis",
            "Docker",
            "Kubernetes",
            "AWS",
            "Azure",
            "GCP",
            "Machine Learning",
            "Deep Learning",
            "TensorFlow",
            "PyTorch",
            "Scikit-learn",
            "NLP",
            "LLM",
            "LangChain",
            "Git",
            "CI/CD",
            "Linux"
        ]

        self.soft_skill_keywords = [
            "Communication",
            "Leadership",
            "Problem Solving",
            "Teamwork",
            "Collaboration",
            "Critical Thinking",
            "Adaptability",
            "Time Management"
        ]

    async def execute(
        self,
        input_data: Dict[str, Any]
    ) -> Dict[str, Any]:

        job_description = input_data.get(
            "job_description",
            ""
        )

        jd_lower = job_description.lower()

        # -----------------------
        # Detect Role
        # -----------------------

        role = "Software Engineer"

        role_patterns = [
            "ai ml engineer",
            "machine learning engineer",
            "data scientist",
            "backend engineer",
            "backend developer",
            "frontend developer",
            "full stack developer",
            "devops engineer",
            "python developer"
        ]

        for pattern in role_patterns:
            if pattern in jd_lower:
                role = pattern.title()
                break

        # -----------------------
        # Detect Seniority
        # -----------------------

        seniority = "Junior"

        if any(
            word in jd_lower
            for word in ["senior", "lead", "principal"]
        ):
            seniority = "Senior"

        elif any(
            word in jd_lower
            for word in ["mid", "intermediate"]
        ):
            seniority = "Mid-Level"

        # -----------------------
        # Extract Skills
        # -----------------------

        required_skills = []

        for skill in self.skill_keywords:

            if skill.lower() in jd_lower:
                required_skills.append(skill)

        required_skills = list(
            dict.fromkeys(required_skills)
        )

        # -----------------------
        # Soft Skills
        # -----------------------

        soft_skills = []

        for skill in self.soft_skill_keywords:

            if skill.lower() in jd_lower:
                soft_skills.append(skill)

        # -----------------------
        # Interview Areas
        # -----------------------

        interview_focus_areas = []

        if "python" in jd_lower:
            interview_focus_areas.append(
                "Python Programming"
            )

        if "fastapi" in jd_lower:
            interview_focus_areas.append(
                "FastAPI Development"
            )

        if "machine learning" in jd_lower:
            interview_focus_areas.append(
                "Machine Learning"
            )

        if "docker" in jd_lower:
            interview_focus_areas.append(
                "Docker"
            )

        if "aws" in jd_lower:
            interview_focus_areas.append(
                "AWS"
            )

        if "kubernetes" in jd_lower:
            interview_focus_areas.append(
                "Kubernetes"
            )

        if not interview_focus_areas:
            interview_focus_areas.append(
                "Technical Fundamentals"
            )

        # -----------------------
        # Summary
        # -----------------------

        job_summary = (
            f"{role} position requiring "
            f"{len(required_skills)} technical skills."
        )

        return {
            "role": role,
            "seniority": seniority,
            "required_skills": required_skills,
            "optional_skills": [],
            "soft_skills": soft_skills,
            "interview_focus_areas": interview_focus_areas,
            "job_summary": job_summary,
        }