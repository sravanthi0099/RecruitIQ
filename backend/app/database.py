from sqlalchemy import create_engine
from sqlalchemy.orm import (
    declarative_base,
    sessionmaker,
)

from app.config import settings

engine = create_engine(
    settings.DATABASE_URL,
    echo=settings.DATABASE_ECHO,
    future=True,
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

Base = declarative_base()


def get_db():
    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


def init_db():

    from app.models.user import User
    from app.models.candidate import Candidate
    from app.models.job import Job
    from app.models.resume import Resume
    from app.models.agent_result import AgentResult
    from app.models.analysis_result import AnalysisResult
    from app.models.interview_result import InterviewResult
    from app.models.ai_analysis import AIAnalysis
    from app.models.interview_response import InterviewResponse
    from app.models.interview_session import InterviewSession
    from app.models.voice_interview_result import VoiceInterviewResult

    Base.metadata.create_all(bind=engine)