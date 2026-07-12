import google.generativeai as genai

from app.config import settings
from app.services.json_utils import extract_json


genai.configure(
    api_key=settings.GEMINI_API_KEY
)


class GeminiService:

    def __init__(self):

        self.model = genai.GenerativeModel(
            "gemini-2.5-flash"
        )

    async def generate_text(
        self,
        prompt: str,
    ) -> str:

        try:

            response = self.model.generate_content(
                prompt
            )

            return response.text

        except Exception as e:

            print(
                "Gemini generate_text failed:",
                str(e)
            )

            return ""

    async def generate_json(
        self,
        prompt: str,
    ):
        """
        Returns the parsed JSON from Gemini's reply.

        On failure this returns {"error": ..., "overall_score": 0} rather
        than silently falling back to Groq's answer relabeled as Gemini's
        -- a caller comparing multiple LLMs needs to know a model actually
        failed, not receive a duplicate score under the wrong name.
        """

        try:

            response = self.model.generate_content(
                prompt
            )

        except Exception as e:

            print(
                "Gemini API call failed:",
                str(e)
            )

            return {
                "error": str(e),
                "overall_score": 0,
            }

        text = response.text.strip()

        return extract_json(text)


gemini_service = GeminiService()
