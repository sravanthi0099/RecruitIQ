import asyncio

from app.agents.ai_candidate_ranker import (
    AICandidateRanker
)


async def main():

    ranker = AICandidateRanker()

    result = await ranker.execute(
        {
            "candidate_profile": {
                "candidate_level": "Junior",
                "strengths": [
                    "Python",
                    "FastAPI",
                    "Docker"
                ]
            },

            "job_profile": {
                "role": "Backend Engineer",
                "required_skills": [
                    "Python",
                    "FastAPI",
                    "Docker",
                    "AWS",
                    "Kubernetes"
                ]
            },

           "skill_gap_profile": {
    "match_score": 60,
    "matching_skills": [
        "Python",
        "FastAPI",
        "Docker"
    ],
    "missing_skills": [
        "AWS",
        "Kubernetes"
    ]
}
            }
    )

    print(result)


if __name__ == "__main__":
    asyncio.run(main())