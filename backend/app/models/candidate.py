"""Candidate database model."""

from sqlalchemy import Column, String, Integer, DateTime, Float, JSON, Text, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from datetime import datetime

from app.database import Base


class Candidate(Base):
    """Candidate model."""

    __tablename__ = "candidates"

    id = Column(String(36), primary_key=True, index=True)
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False, index=True)
    
    # Basic Information
    first_name = Column(String(255), nullable=False)
    last_name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    phone = Column(String(20), nullable=True)
    location = Column(String(255), nullable=True)
    
    # Resume Information
    resume_url = Column(String(1024), nullable=True)
    resume_text = Column(Text, nullable=True)
    resume_embedding = Column(Text, nullable=True) # Stored as JSON
    
    # Analysis Results
    extracted_skills = Column(JSON, default={}, nullable=False)
    years_of_experience = Column(Float, nullable=True)
    education = Column(JSON, default=[], nullable=False)
    
    # Status
    status = Column(String(50), default="new", nullable=False)  # new, screening, interview, offer, rejected
    match_score = Column(Float, nullable=True)
    
    # Metadata
    notes = Column(Text, nullable=True)
    custom_fields = Column(JSON, default={}, nullable=False)
    
    # Timestamps
    created_at = Column(DateTime, server_default=func.now(), nullable=False, index=True)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # Relationships
    resumes = relationship("Resume", back_populates="candidate", cascade="all, delete-orphan")
    agent_results = relationship("AgentResult", back_populates="candidate", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<Candidate(id={self.id}, email={self.email}, years_exp={self.years_of_experience})>"