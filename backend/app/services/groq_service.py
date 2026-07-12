from groq import Groq

from app.config import settings
from app.services.json_utils import extract_json


class GroqService:

    def __init__(self):

        self.client = Groq(
            api_key=settings.GROQ_API_KEY
        )

    async def generate_json(
        self,
        prompt: str
    ):

        try:
            response = self.client.chat.completions.create(
                model="llama-3.3-70b-versatile",
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
                temperature=0.3
            )
        except Exception as e:
            print("Groq API call failed:", str(e))
            return {"error": str(e), "overall_score": 0}

        text = (
            response
            .choices[0]
            .message.content
            .strip()
        )

        print("\n========== GROQ RAW RESPONSE ==========\n")
        print(text)
        print("\n=======================================\n")

        return extract_json(text)


groq_service = GroqService()
