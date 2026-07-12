"""RecruitIQ Voice Interview Evaluator Agent.

Extends the existing text-based InterviewEvaluatorAgent: same JSON scoring
contract, but the prompt is enriched with speech-delivery metrics (pace,
filler words, hesitation) and an optional camera-derived engagement score,
so the LLM can factor delivery/confidence into its scoring rather than
judging transcript text alone.
"""

from app.agents.base_agent import BaseAgent
from app.services.groq_service import groq_service


class VoiceInterviewEvaluatorAgent(BaseAgent):

    def __init__(self):
        super().__init__(
            name="VoiceInterviewEvaluatorAgent",
            version="1.0.0",
        )

    async def execute(self, input_data):

        question = input_data.get("question", "")
        transcript = input_data.get("transcript", "")
        job_role = input_data.get("job_role", "")

        speaking_pace_wpm = input_data.get("speaking_pace_wpm", 0)
        filler_word_count = input_data.get("filler_word_count", 0)
        long_pause_count = input_data.get("long_pause_count", 0)
        duration_seconds = input_data.get("duration_seconds", 0)

        # Optional, browser-derived, best-effort — 0-100, may be None if
        # the candidate's browser doesn't support face detection.
        eye_contact_score = input_data.get("eye_contact_score")

        pace_note = (
            "too fast" if speaking_pace_wpm > 170 else
            "too slow" if 0 < speaking_pace_wpm < 90 else
            "within a natural conversational range"
        )

        prompt = f"""
You are a Senior Technical Interviewer evaluating a LIVE SPOKEN answer
(transcribed via speech-to-text), not a written one.

Job Role:
{job_role}

Question:
{question}

Transcribed Candidate Answer:
{transcript}

Speech Delivery Signals:
- Duration: {duration_seconds} seconds
- Speaking pace: {speaking_pace_wpm} words per minute ({pace_note})
- Filler words detected ("um", "like", "uh", etc.): {filler_word_count}
- Long hesitation pauses (>1.5s): {long_pause_count}
- Camera-based engagement/eye-contact score (0-100, best-effort, may be
  absent): {eye_contact_score if eye_contact_score is not None else "not available"}

Instructions:
1. Evaluate technical correctness and depth from the transcript content.
2. Let filler words, pace, and hesitation pull down "communication_score"
   and "confidence_score" — but do not penalize harshly for a handful of
   fillers, since natural speech always has some.
3. If the transcript looks garbled or clearly mistranscribed in places, be
   lenient on wording/grammar and focus on substance.
4. If an engagement/eye-contact score is available, treat it as one minor
   input into "confidence_score", not the deciding factor.

Return ONLY valid JSON in this exact shape:

{{
    "technical_score": 0-100,
    "communication_score": 0-100,
    "problem_solving_score": 0-100,
    "confidence_score": 0-100,
    "overall_score": 0-100,
    "strengths": [],
    "weaknesses": [],
    "feedback": "",
    "recommendation": "Pass or Fail"
}}
"""

        try:
            result = await groq_service.generate_json(prompt)

            result["transcript"] = transcript
            result["speaking_pace_wpm"] = speaking_pace_wpm
            result["filler_word_count"] = filler_word_count
            result["long_pause_count"] = long_pause_count
            result["eye_contact_score"] = eye_contact_score

            return result

        except Exception as e:

            print("Voice Interview Evaluation Error:", str(e))

            return {
                "technical_score": 0,
                "communication_score": 0,
                "problem_solving_score": 0,
                "confidence_score": 0,
                "overall_score": 0,
                "strengths": [],
                "weaknesses": [],
                "feedback": str(e),
                "recommendation": "Fail",
                "transcript": transcript,
                "speaking_pace_wpm": speaking_pace_wpm,
                "filler_word_count": filler_word_count,
                "long_pause_count": long_pause_count,
                "eye_contact_score": eye_contact_score,
            }
