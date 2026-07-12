"""Agent analysis results database model."""

from sqlalchemy import (
    Column,
    String,
    DateTime,
    JSON,
    Text,
    ForeignKey,
    Float,
    Integer,
)
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.database import Base


class AgentResult(Base):
    """Agent analysis results model."""

    __tablename__ = "agent_results"

    id = Column(String(36), primary_key=True, index=True)

    candidate_id = Column(
        String(36),
        ForeignKey("candidates.id"),
        nullable=False,
        index=True,
    )

    job_id = Column(
        String(36),
        ForeignKey("jobs.id"),
        nullable=True,
        index=True,
    )

    # Agent Information
    agent_type = Column(
        String(50),
        nullable=False,
        index=True,
    )

    agent_version = Column(
        String(50),
        nullable=True,
    )

    # Results
    analysis_result = Column(
        JSON,
        default=dict,
        nullable=False,
    )

    recommendations = Column(
        JSON,
        default=list,
        nullable=False,
    )

    # Scoring
    confidence_score = Column(
        Float,
        nullable=True,
    )

    relevance_score = Column(
        Float,
        nullable=True,
    )

    # Metadata
    model_used = Column(
        String(255),
        nullable=True,
    )

    processing_time_ms = Column(
        Integer,
        nullable=True,
    )

    tokens_used = Column(
        Integer,
        nullable=True,
    )

    # Error Handling
    status = Column(
        String(50),
        default="completed",
        nullable=False,
    )

    error_message = Column(
        Text,
        nullable=True,
    )

    # Timestamps
    created_at = Column(
        DateTime,
        server_default=func.now(),
        nullable=False,
        index=True,
    )

    executed_at = Column(
        DateTime,
        nullable=True,
    )

    # Relationships
    candidate = relationship(
        "Candidate",
        back_populates="agent_results",
    )

    def __repr__(self) -> str:
        return (
            f"<AgentResult(id={self.id}, "
            f"agent_type={self.agent_type}, "
            f"status={self.status})>"
        )