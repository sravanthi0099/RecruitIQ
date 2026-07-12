from sqlalchemy import (
    Column,
    String,
    Float,
    Integer,
    DateTime,
    Text,
)

from sqlalchemy.sql import func

from app.database import Base


class VoiceInterviewResult(Base):
    """Stores results from the live voice + camera interview mode.

    Kept as its own table (rather than adding columns to
    `interview_results`) so this feature can be added without an Alembic
    migration touching the existing table.
    """

    __tablename__ = "voice_interview_results"

    id = Column(String(36), primary_key=True)

    candidate_id = Column(String(36), nullable=False)
    job_id = Column(String(36), nullable=False)

    question = Column(Text, nullable=False)
    transcript = Column(Text, nullable=False)

    duration_seconds = Column(Float, default=0)
    speaking_pace_wpm = Column(Float, default=0)
    filler_word_count = Column(Integer, default=0)
    long_pause_count = Column(Integer, default=0)
    eye_contact_score = Column(Float, nullable=True)

    technical_score = Column(Float, default=0)
    communication_score = Column(Float, default=0)
    problem_solving_score = Column(Float, default=0)
    confidence_score = Column(Float, default=0)
    overall_score = Column(Float, default=0)

    recommendation = Column(String(50))
    feedback = Column(Text)

    created_at = Column(DateTime, server_default=func.now())
