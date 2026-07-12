from cerebras.cloud.sdk import Cerebras

from app.config import settings
from app.services.json_utils import extract_json


class CerebrasService:

    def __init__(self):

        self.client = Cerebras(
            api_key=settings.CEREBRAS_API_KEY
        )

    async def generate_json(
        self,
        prompt: str
    ):

        try:
            response = (
                self.client.chat.completions.create(
                    messages=[
                        {
                            "role": "system",
                            "content":
                            "Return ONLY valid JSON. No markdown. No explanations."
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    model="gpt-oss-120b"
                )
            )
        except Exception as e:
            print("Cerebras API call failed:", str(e))
            return {"error": str(e), "overall_score": 0}

        text = (
            response
            .choices[0]
            .message.content
            .strip()
        )

        return extract_json(text)


cerebras_service = CerebrasService()