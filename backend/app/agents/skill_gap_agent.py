from typing import Dict, Any

from app.agents.base_agent import BaseAgent
from app.services.gemini_service import gemini_service


class SkillGapAgent(BaseAgent):
    """AI Skill Gap Intelligence Agent."""

    def __init__(self):
        super().__init__(
            name="SkillGapAgent",
            version="1.0.0"
        )

    async def execute(
        self,
        input_data: Dict[str, Any]
    ) -> Dict[str, Any]:

        candidate_skills = input_data.get(
            "candidate_skills",
            []
        )

        required_skills = input_data.get(
            "required_skills",
            []
        )

        candidate_level = input_data.get(
            "candidate_level",
            "Junior"
        )

        # deterministic matching
        candidate_set = {
            skill.strip().lower()
            for skill in candidate_skills
        }

        required_set = {
            skill.strip().lower()
            for skill in required_skills
        }

        matching_skills = [
            skill
            for skill in required_skills
            if skill.lower() in candidate_set
        ]

        missing_skills = [
            skill
            for skill in required_skills
            if skill.lower() not in candidate_set
        ]

        if len(required_skills) > 0:
            match_score = int(
                (
                    len(matching_skills)
                    / len(required_skills)
                ) * 100
            )
        else:
            match_score = 0

        prompt = f"""
Candidate Level:
{candidate_level}

Matching Skills:
{matching_skills}

Missing Skills:
{missing_skills}

Match Score:
{match_score}

Return ONLY valid JSON.

{{
    "learning_priority": [],
    "estimated_readiness": "",
    "hire_recommendation": "",
    "reasoning": ""
}}
"""

        return {
    "match_score": match_score,
    "matching_skills": matching_skills,
    "missing_skills": missing_skills,
    "learning_priority": missing_skills,
    "estimated_readiness": (
        "High"
        if match_score >= 80
        else "Medium"
        if match_score >= 60
        else "Low"
    ),
    "hire_recommendation": (
        "Strong Hire"
        if match_score >= 80
        else "Consider"
        if match_score >= 60
        else "Reject"
    ),
    "reasoning":
    f"Matched {len(matching_skills)} out of "
    f"{len(required_skills)} required skills."
}

        