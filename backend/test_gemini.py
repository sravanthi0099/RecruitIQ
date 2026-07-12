import asyncio

from app.services.gemini_service import (
    gemini_service
)


async def main():

    result = await gemini_service.generate_text(
        """
        Explain FastAPI in one paragraph.
        """
    )

    print(result)


asyncio.run(main())