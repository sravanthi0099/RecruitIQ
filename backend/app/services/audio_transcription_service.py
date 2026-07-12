"""
Audio Transcription Service
----------------------------
Transcribes a candidate's spoken interview answer and derives simple
speech-delivery signals (pace, filler words, pause count) that feed into
the interview evaluator agent alongside the text of the answer.

Uses Groq's hosted Whisper endpoint (whisper-large-v3-turbo) because
RecruitIQ already depends on `groq` for text generation, so no new API
key or paid service is required.
"""

import io
import re
from typing import Dict, Any

from groq import Groq

from app.config import settings


FILLER_WORDS = [
    "um", "uh", "umm", "uhh", "like", "you know", "so yeah",
    "i mean", "actually", "basically", "kind of", "sort of",
]


class AudioTranscriptionService:

    def __init__(self):
        self.client = Groq(api_key=settings.GROQ_API_KEY)

    async def transcribe(
        self,
        audio_bytes: bytes,
        filename: str = "answer.webm",
    ) -> Dict[str, Any]:
        """
        Transcribe raw audio bytes and compute delivery metrics.

        Returns:
            {
                "transcript": str,
                "duration_seconds": float,
                "word_count": int,
                "speaking_pace_wpm": float,
                "filler_word_count": int,
                "long_pause_count": int,
            }
        """

        audio_file = io.BytesIO(audio_bytes)
        audio_file.name = filename

        response = self.client.audio.transcriptions.create(
            file=audio_file,
            model="whisper-large-v3-turbo",
            response_format="verbose_json",
        )

        transcript = (response.text or "").strip()
        segments = getattr(response, "segments", None) or []
        duration = getattr(response, "duration", None)

        if not duration:
            # Fall back to last segment end time if the API omits duration
            duration = segments[-1]["end"] if segments else 0.0

        word_count = len(transcript.split()) if transcript else 0

        speaking_pace_wpm = (
            round((word_count / duration) * 60, 1)
            if duration and duration > 0
            else 0.0
        )

        filler_word_count = self._count_filler_words(transcript)
        long_pause_count = self._count_long_pauses(segments)

        return {
            "transcript": transcript,
            "duration_seconds": round(duration, 1) if duration else 0.0,
            "word_count": word_count,
            "speaking_pace_wpm": speaking_pace_wpm,
            "filler_word_count": filler_word_count,
            "long_pause_count": long_pause_count,
        }

    def _count_filler_words(self, transcript: str) -> int:
        if not transcript:
            return 0

        text_lower = transcript.lower()
        count = 0

        for filler in FILLER_WORDS:
            count += len(
                re.findall(rf"\b{re.escape(filler)}\b", text_lower)
            )

        return count

    def _count_long_pauses(self, segments, threshold_seconds: float = 1.5) -> int:
        """Counts gaps between consecutive Whisper segments longer than
        `threshold_seconds`, used as a rough proxy for hesitation."""

        if not segments or len(segments) < 2:
            return 0

        pause_count = 0

        for prev, curr in zip(segments, segments[1:]):
            gap = curr.get("start", 0) - prev.get("end", 0)
            if gap >= threshold_seconds:
                pause_count += 1

        return pause_count


audio_transcription_service = AudioTranscriptionService()
