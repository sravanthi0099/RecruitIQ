from typing import Dict, Any

from app.agents.base_agent import BaseAgent

from app.services.gemini_service import (
    gemini_service
)

from app.services.groq_service import (
    groq_service
)


class AIResumeAgent(BaseAgent):
    """AI-powered resume intelligence agent."""

    def __init__(self):
        super().__init__(
            name="AIResumeAgent",
            version="1.0.0"
        )

    async def execute(
        self,
        input_data: Dict[str, Any]
    ) -> Dict[str, Any]:

        resume_text = input_data.get(
            "resume_text",
            ""
        )

        prompt = f"""
Analyze the following resume.

Return ONLY valid JSON.

{{
    "candidate_level": "",
    "skills": [],
    "experience_years": 0,
    "strengths": [],
    "weaknesses": [],
    "recommended_roles": [],
    "skill_gaps": [],
    "career_summary": ""
}}

Resume:

{resume_text}
"""

        try:

            result = await gemini_service.generate_json(
                prompt
            )

        except Exception as e:

            print(
                "Gemini Resume Analysis Failed:",
                str(e)
            )

            result = await groq_service.generate_json(
                prompt
            )

        if "skills" not in result:
            result["skills"] = []

        if "experience_years" not in result:
            result["experience_years"] = 0

        if "candidate_level" not in result:
            result["candidate_level"] = "Junior"

        return result