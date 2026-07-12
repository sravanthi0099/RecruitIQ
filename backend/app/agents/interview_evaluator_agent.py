import json

from app.agents.base_agent import BaseAgent
from app.services.groq_service import groq_service


class InterviewEvaluatorAgent(BaseAgent):

    def __init__(self):

        super().__init__(
            name="InterviewEvaluatorAgent",
            version="1.0.0"
        )

    async def execute(
        self,
        input_data
    ):

        question = input_data.get(
            "question",
            ""
        )

        answer = input_data.get(
            "answer",
            ""
        )

        job_role = input_data.get(
            "job_role",
            ""
        )

        prompt = f"""
You are a Senior Technical Interviewer.

Job Role:
{job_role}

Question:
{question}

Candidate Answer:
{answer}

Evaluate the answer.

Return ONLY valid JSON.

{{
    "technical_score": 0-100,
    "communication_score": 0-100,
    "problem_solving_score": 0-100,
    "confidence_score": 0-100,
    "overall_score": 0-100,
    "strengths": [],
    "weaknesses": [],
    "feedback": "",
    "recommendation": "Pass or Fail"
}}
"""

        try:

            result = await groq_service.generate_json(
                prompt
            )

            return result

        except Exception as e:

            print(
                "Interview Evaluation Error:",
                str(e)
            )

            return {
                "technical_score": 0,
                "communication_score": 0,
                "problem_solving_score": 0,
                "confidence_score": 0,
                "overall_score": 0,
                "strengths": [],
                "weaknesses": [],
                "feedback": str(e),
                "recommendation": "Fail"
            }