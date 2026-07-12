from sqlalchemy import (
    Column,
    String,
    Float,
    Text,
    DateTime
)

from sqlalchemy.sql import func

from app.database import Base


class InterviewSession(Base):

    __tablename__ = "interview_session"

    id = Column(
        String,
        primary_key=True
    )

    candidate_id = Column(
        String,
        nullable=False
    )

    job_id = Column(
        String,
        nullable=False
    )

    question = Column(
        Text,
        nullable=False
    )

    answer = Column(
        Text,
        nullable=True
    )

    score = Column(
        Float,
        default=0
    )

    recommendation = Column(
        String,
        default="Pending"
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )