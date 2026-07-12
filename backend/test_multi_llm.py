import asyncio

from app.agents.multi_llm_evaluator import (
    MultiLLMEvaluator
)


async def main():

    agent = (
        MultiLLMEvaluator()
    )

    result = await agent.execute(
        {
            "job_role":
            "AI ML Engineer",

            "question":
            "What is overfitting?",

            "answer":
            """
Overfitting occurs when a model
learns training data too closely
and performs poorly on unseen data.
It can be reduced using
cross validation,
regularization,
and more training data.
"""
        }
    )

    print(result)


asyncio.run(main())