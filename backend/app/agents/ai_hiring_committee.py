from typing import Dict, Any

from app.agents.base_agent import BaseAgent
from app.services.groq_service import groq_service


class AIHiringCommittee(BaseAgent):

    def __init__(self):
        super().__init__(
            name="AIHiringCommittee",
            version="1.0.0"
        )

    async def execute(
        self,
        input_data: Dict[str, Any]
    ) -> Dict[str, Any]:

        resume_analysis = input_data.get(
            "resume_analysis",
            {}
        )

        job_analysis = input_data.get(
            "job_analysis",
            {}
        )

        skill_gap_analysis = input_data.get(
            "skill_gap_analysis",
            {}
        )

        candidate_ranking = input_data.get(
            "candidate_ranking",
            {}
        )

        prompt = f"""
You are an AI Hiring Committee.

Review:

1. Resume Analysis
2. Job Analysis
3. Skill Gap Analysis
4. Candidate Ranking

Return ONLY valid JSON.

{{
    "committee_decision":"",
    "confidence_score":0,
    "pros":[],
    "cons":[],
    "final_reasoning":""
}}

Resume Analysis:
{resume_analysis}

Job Analysis:
{job_analysis}

Skill Gap Analysis:
{skill_gap_analysis}

Candidate Ranking:
{candidate_ranking}
"""

        result = await groq_service.generate_json(
            prompt
        )

        return result