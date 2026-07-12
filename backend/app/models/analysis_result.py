from sqlalchemy import Column, String, JSON, DateTime
from sqlalchemy.sql import func

from app.database import Base


class AnalysisResult(Base):

    __tablename__ = "analysis_results"

    id = Column(String(36), primary_key=True)

    candidate_id = Column(String(36))
    job_id = Column(String(36))

    resume_analysis = Column(JSON)
    job_analysis = Column(JSON)
    skill_gap_analysis = Column(JSON)
    candidate_ranking = Column(JSON)

    interview_questions = Column(JSON)

    committee_result = Column(JSON)

    final_decision = Column(String(100))

    created_at = Column(
        DateTime,
        server_default=func.now()
    )