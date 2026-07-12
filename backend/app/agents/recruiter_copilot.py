from app.agents.base_agent import BaseAgent
from app.services.groq_service import groq_service


class RecruiterCopilot(BaseAgent):

    def __init__(self):

        super().__init__(
            name="RecruiterCopilot",
            version="1.0.0"
        )

    async def execute(
        self,
        input_data
    ):

        recruiter_question = input_data.get(
            "question",
            ""
        )

        context = input_data.get(
            "context",
            {}
        )

        prompt = f"""
You are RecruitIQ Recruiter Copilot.

You help recruiters make hiring decisions.

Available Data:

{context}

Recruiter Question:

{recruiter_question}

Answer as a senior hiring consultant.

Provide:

1. Direct Answer
2. Reasoning
3. Recommendation
"""

        result = await groq_service.generate_json(
            f"""
Return ONLY JSON

{{
    "answer":"",
    "reasoning":"",
    "recommendation":""
}}

{prompt}
"""
        )

        return result