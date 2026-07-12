from uuid import uuid4

from fastapi import APIRouter
from fastapi import Depends
from fastapi import UploadFile
from fastapi import File
from fastapi import Form

from sqlalchemy.orm import Session

from app.database import get_db
from app.api.auth import get_authenticated_user
from app.models.user import User

from app.models.interview_result import (
    InterviewResult
)

from app.models.voice_interview_result import (
    VoiceInterviewResult
)

from app.models.job import Job

from app.agents.interview_evaluator_agent import (
    InterviewEvaluatorAgent
)

from app.agents.voice_interview_evaluator_agent import (
    VoiceInterviewEvaluatorAgent
)

from app.services.audio_transcription_service import (
    audio_transcription_service
)

router = APIRouter(
    prefix="/api/interview",
    tags=["Interview"]
)


@router.post(
    "/evaluate-answer"
)
async def evaluate_answer(

    candidate_id: str,
    job_id: str,
    question: str,
    answer: str,

    current_user: User = Depends(
        get_authenticated_user
    ),

    db: Session = Depends(
        get_db
    )

):

    job = (
        db.query(Job)
        .filter(
            Job.id == job_id
        )
        .first()
    )

    if not job:

        return {
            "error":
            "Job not found"
        }

    evaluator = (
        InterviewEvaluatorAgent()
    )

    result = await evaluator.execute(
        {
            "question":
            question,

            "answer":
            answer,

            "job_role":
            job.title
        }
    )

    record = InterviewResult(
        id=str(uuid4()),
        candidate_id=candidate_id,
        job_id=job_id,
        question=question,
        answer=answer,
        technical_score=result.get(
            "technical_score",
            0
        ),
        communication_score=result.get(
            "communication_score",
            0
        ),
        problem_solving_score=result.get(
            "problem_solving_score",
            0
        ),
        confidence_score=result.get(
            "confidence_score",
            0
        ),
        overall_score=result.get(
            "overall_score",
            0
        ),
        recommendation=result.get(
            "recommendation",
            "Fail"
        ),
        feedback=result.get(
            "feedback",
            ""
        )
    )

    db.add(record)
    db.commit()

    return result


@router.post(
    "/evaluate-voice-answer"
)
async def evaluate_voice_answer(

    candidate_id: str = Form(...),
    job_id: str = Form(...),
    question: str = Form(...),
    audio: UploadFile = File(...),
    eye_contact_score: float = Form(None),

    current_user: User = Depends(
        get_authenticated_user
    ),

    db: Session = Depends(
        get_db
    )

):
    """
    Live voice + camera interview answer.

    The frontend records the candidate's spoken answer (audio) while the
    camera preview is used client-side for a best-effort engagement score
    (`eye_contact_score`, 0-100, optional). This endpoint:

    1. Transcribes the audio with Whisper (Groq).
    2. Derives speech-delivery metrics (pace, filler words, pauses).
    3. Runs the transcript + metrics through the voice evaluator agent.
    4. Persists and returns the combined result.
    """

    job = (
        db.query(Job)
        .filter(
            Job.id == job_id
        )
        .first()
    )

    if not job:

        return {
            "error":
            "Job not found"
        }

    audio_bytes = await audio.read()

    if not audio_bytes:
        return {
            "error":
            "No audio received. Please record an answer before submitting."
        }

    transcription = await audio_transcription_service.transcribe(
        audio_bytes,
        filename=audio.filename or "answer.webm",
    )

    if not transcription.get("transcript"):
        return {
            "error":
            "Could not transcribe audio. Please check your microphone and try again."
        }

    evaluator = VoiceInterviewEvaluatorAgent()

    result = await evaluator.execute(
        {
            "question": question,
            "transcript": transcription["transcript"],
            "job_role": job.title,
            "speaking_pace_wpm": transcription["speaking_pace_wpm"],
            "filler_word_count": transcription["filler_word_count"],
            "long_pause_count": transcription["long_pause_count"],
            "duration_seconds": transcription["duration_seconds"],
            "eye_contact_score": eye_contact_score,
        }
    )

    record = VoiceInterviewResult(
        id=str(uuid4()),
        candidate_id=candidate_id,
        job_id=job_id,
        question=question,
        transcript=transcription["transcript"],
        duration_seconds=transcription["duration_seconds"],
        speaking_pace_wpm=transcription["speaking_pace_wpm"],
        filler_word_count=transcription["filler_word_count"],
        long_pause_count=transcription["long_pause_count"],
        eye_contact_score=eye_contact_score,
        technical_score=result.get("technical_score", 0),
        communication_score=result.get("communication_score", 0),
        problem_solving_score=result.get("problem_solving_score", 0),
        confidence_score=result.get("confidence_score", 0),
        overall_score=result.get("overall_score", 0),
        recommendation=result.get("recommendation", "Fail"),
        feedback=result.get("feedback", ""),
    )

    db.add(record)
    db.commit()

    return result


@router.get("/report/{candidate_id}")
async def interview_report(
    candidate_id: str,
    current_user: User = Depends(get_authenticated_user),
    db: Session = Depends(get_db)
):

    responses = (
        db.query(InterviewResult)
        .filter(
            InterviewResult.candidate_id
            == candidate_id
        )
        .all()
    )

    if not responses:
        return {
            "error":
            "No interview results found"
        }

    total_score = sum(
        r.overall_score
        for r in responses
    )

    avg_score = round(
        total_score /
        len(responses),
        2
    )

    return {
        "candidate_id":
        candidate_id,

        "total_questions":
        len(responses),

        "average_score":
        avg_score,

        "recommendation":
        (
            "Strong Hire"
            if avg_score >= 85 else
            "Hire"
            if avg_score >= 70 else
            "Consider"
            if avg_score >= 50 else
            "Reject"
        ),

        "responses":
        [
            {
                "question":
                r.question,

                "score":
                r.overall_score,

                "feedback":
                r.feedback
            }
            for r in responses
        ]
    }
