from sqlalchemy import (
    Column,
    String,
    Float,
    Text,
    DateTime
)

from sqlalchemy.sql import func

from app.database import Base


class InterviewResponse(Base):

    __tablename__ = "interview_responses"

    id = Column(
        String,
        primary_key=True
    )

    candidate_id = Column(String)

    job_id = Column(String)

    question = Column(Text)

    answer = Column(Text)

    groq_score = Column(Float)

    gemini_score = Column(Float)

    cerebras_score = Column(Float)

    final_score = Column(Float)

    recommendation = Column(String)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )