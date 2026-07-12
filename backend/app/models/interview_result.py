from sqlalchemy import (
    Column,
    String,
    Float,
    DateTime,
    Text
)

from sqlalchemy.sql import func

from app.database import Base


class InterviewResult(Base):

    __tablename__ = "interview_results"

    id = Column(
        String(36),
        primary_key=True
    )

    candidate_id = Column(
        String(36),
        nullable=False
    )

    job_id = Column(
        String(36),
        nullable=False
    )

    question = Column(
        Text,
        nullable=False
    )

    answer = Column(
        Text,
        nullable=False
    )

    technical_score = Column(
        Float,
        default=0
    )

    communication_score = Column(
        Float,
        default=0
    )

    problem_solving_score = Column(
        Float,
        default=0
    )

    confidence_score = Column(
        Float,
        default=0
    )

    overall_score = Column(
        Float,
        default=0
    )

    recommendation = Column(
        String(50)
    )

    feedback = Column(
        Text
    )

    created_at = Column(
        DateTime,
        server_default=func.now()
    )