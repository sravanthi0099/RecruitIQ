from sqlalchemy import Column, String, Text, JSON, DateTime
from sqlalchemy.sql import func

from app.database import Base


class AIAnalysis(Base):

    __tablename__ = "ai_analysis"

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

    resume_analysis = Column(JSON)

    job_analysis = Column(JSON)

    skill_gap_analysis = Column(JSON)

    candidate_ranking = Column(JSON)

    interview_questions = Column(JSON)

    committee_result = Column(JSON)

    final_decision = Column(String)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )