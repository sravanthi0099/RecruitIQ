import asyncio

from app.agents.gemini_interview_agent import (
    GeminiInterviewAgent
)


async def main():

    agent = GeminiInterviewAgent()

    result = await agent.execute(
        {
            "candidate_profile": {
                "candidate_level": "Junior",
                "skills": [
                    "Python",
                    "FastAPI",
                    "Docker"
                ],
                "experience_years": 2
            },

            "job_profile": {
                "role": "Backend Engineer",
                "required_skills": [
                    "Python",
                    "FastAPI",
                    "AWS",
                    "Kubernetes"
                ]
            },

            "skill_gap_profile": {
                "match_score": 60,
                "missing_skills": [
                    "AWS",
                    "Kubernetes"
                ]
            },

            "difficulty": "medium",
            "num_questions": 10
        }
    )

    print("\nFINAL RESULT\n")
    print(result)


if __name__ == "__main__":
    asyncio.run(main())