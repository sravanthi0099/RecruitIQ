import asyncio

from app.agents.jd_agent import JDAgent


async def main():

    agent = JDAgent()

    result = await agent.execute(
        {
            "job_description": """
We are looking for a Backend Engineer.

Requirements:

Python
FastAPI
Docker
AWS

Nice to have:

Kubernetes
CI/CD

Experience: 2-4 years
"""
        }
    )

    print(result)


if __name__ == "__main__":
    asyncio.run(main())