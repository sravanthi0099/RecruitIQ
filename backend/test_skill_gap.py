import asyncio

from app.agents.skill_gap_agent import (
    SkillGapAgent
)


async def main():

    agent = SkillGapAgent()

    candidate_profile = {
        "candidate_level": "Junior",
        "strengths": [
            "Python",
            "FastAPI",
            "Docker"
        ]
    }

    job_profile = {
        "role": "Backend Engineer",
        "required_skills": [
            "Python",
            "FastAPI",
            "Docker",
            "AWS",
            "Kubernetes"
        ]
    }

    result = await agent.execute(
        {
            "candidate_profile":
            candidate_profile,
            "job_profile":
            job_profile,
        }
    )

    print(result)


if __name__ == "__main__":
    asyncio.run(main())