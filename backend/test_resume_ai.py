import asyncio

from app.agents.ai_resume_agent import AIResumeAgent


async def main():

    agent = AIResumeAgent()

    result = await agent.execute(
        {
            "resume_text": """
Python
FastAPI
Docker
AWS

Built REST APIs.

2 years experience.
"""
        }
    )

    print(result)


if __name__ == "__main__":
    asyncio.run(main())