import asyncio

from app.agents.gemini_interview_agent import (
    GeminiInterviewAgent
)


async def main():

    agent = GeminiInterviewAgent()

    result = await agent.execute(
        {
            "candidate_profile": {
                "strengths": [
                    "Python",
                    "FastAPI",
                    "Docker"
                ]
            },

            "job_profile": {
                "required_skills": [
                    "Python",
                    "FastAPI",
                    "Docker",
                    "AWS",
                    "Kubernetes"
                ]
            },

            "skill_gap_profile": {
                "missing_skills": [
                    "AWS",
                    "Kubernetes"
                ]
            },

            "difficulty": "medium",
            "num_questions": 10
        }
    )

    print(result)


if __name__ == "__main__":
    asyncio.run(main())