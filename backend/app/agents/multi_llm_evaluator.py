from app.agents.base_agent import BaseAgent

from app.services.groq_service import (
    groq_service
)

from app.services.gemini_service import (
    gemini_service
)

from app.services.cerebras_service import (
    cerebras_service
)


class MultiLLMEvaluator(BaseAgent):

    def __init__(self):

        super().__init__(
            name="MultiLLMEvaluator",
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
You are a senior technical interviewer.

Job Role:
{job_role}

Question:
{question}

Answer:
{answer}

Evaluate the answer.

Return ONLY valid JSON.

{{
    "overall_score": 0
}}
"""

        # -------------------
        # GROQ
        # -------------------

        try:

            groq_result = (
                await groq_service.generate_json(
                    prompt
                )
            )

        except Exception as e:

            print(
                "Groq Failed:",
                str(e)
            )

            groq_result = {
                "overall_score": 0
            }

        # -------------------
        # GEMINI
        # -------------------

        try:

            gemini_result = (
                await gemini_service.generate_json(
                    prompt
                )
            )

        except Exception as e:

            print(
                "Gemini Failed:",
                str(e)
            )

            gemini_result = {
                "overall_score": 0
            }

        # -------------------
        # CEREBRAS
        # -------------------

        try:

            cerebras_result = (
                await cerebras_service.generate_json(
                    prompt
                )
            )

        except Exception as e:

            print(
                "Cerebras Failed:",
                str(e)
            )

            cerebras_result = {
                "overall_score": 0
            }

        # -------------------
        # Scores
        # -------------------

        groq_score = float(
            groq_result.get(
                "overall_score",
                0
            )
        ) * 10

        gemini_score = float(
            gemini_result.get(
                "overall_score",
                0
            )
        ) * 10

        cerebras_score = float(
            cerebras_result.get(
                "overall_score",
                0
            )
        ) * 10

        scores = []

        if groq_score > 0:
            scores.append(
                groq_score
            )

        if gemini_score > 0:
            scores.append(
                gemini_score
            )

        if cerebras_score > 0:
            scores.append(
                cerebras_score
            )

        if scores:

            final_score = round(
                sum(scores) /
                len(scores),
                2
            )

        else:

            final_score = 0

        # -------------------
        # Recommendation
        # -------------------

        if final_score >= 85:

            recommendation = (
                "Strong Hire"
            )

        elif final_score >= 70:

            recommendation = (
                "Hire"
            )

        elif final_score >= 50:

            recommendation = (
                "Consider"
            )

        else:

            recommendation = (
                "Reject"
            )

        return {
            "groq_score":
            groq_score,

            "gemini_score":
            gemini_score,

            "cerebras_score":
            cerebras_score,

            "final_score":
            final_score,

            "recommendation":
            recommendation
        }