"""Resume database model."""

from sqlalchemy import (
    Column,
    String,
    Integer,
    DateTime,
    JSON,
    Text,
    ForeignKey,
    Float,
    Boolean,
)
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.database import Base


class Resume(Base):
    """Resume model."""

    __tablename__ = "resumes"

    id = Column(String(36), primary_key=True, index=True)

    candidate_id = Column(
        String(36),
        ForeignKey("candidates.id"),
        nullable=False,
        index=True,
    )

    # File Information
    file_name = Column(
        String(255),
        nullable=False,
    )

    file_url = Column(
        String(1024),
        nullable=False,
    )

    file_size = Column(
        Integer,
        nullable=True,
    )

    # Content
    raw_text = Column(
        Text,
        nullable=False,
    )

    parsed_json = Column(
        JSON,
        default=dict,
        nullable=False,
    )

    # Embeddings
    embedding = Column(
        Text,
        nullable=True,
    )

    embedding_model = Column(
        String(255),
        nullable=True,
    )

    # Extracted Information
    skills = Column(
        JSON,
        default=list,
        nullable=False,
    )

    experience = Column(
        JSON,
        default=list,
        nullable=False,
    )

    education = Column(
        JSON,
        default=list,
        nullable=False,
    )

    certifications = Column(
        JSON,
        default=list,
        nullable=False,
    )

    languages = Column(
        JSON,
        default=list,
        nullable=False,
    )

    # Analysis Results
    readability_score = Column(
        Float,
        nullable=True,
    )

    completeness_score = Column(
        Float,
        nullable=True,
    )

    # Status
    is_parsed = Column(
        Boolean,
        default=False,
        nullable=False,
    )

    parse_status = Column(
        String(50),
        default="pending",
        nullable=False,
    )

    parse_error = Column(
        Text,
        nullable=True,
    )

    # Metadata
    custom_fields = Column(
        JSON,
        default=dict,
        nullable=False,
    )

    # Timestamps
    created_at = Column(
        DateTime,
        server_default=func.now(),
        nullable=False,
        index=True,
    )

    updated_at = Column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    parsed_at = Column(
        DateTime,
        nullable=True,
    )

    # Relationships
    candidate = relationship(
        "Candidate",
        back_populates="resumes",
    )

    def __repr__(self) -> str:
        return (
            f"<Resume(id={self.id}, "
            f"candidate_id={self.candidate_id}, "
            f"file_name={self.file_name})>"
        )