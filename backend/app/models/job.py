"""Job posting database model."""

from sqlalchemy import (
    Column,
    String,
    DateTime,
    Float,
    JSON,
    Text,
    ForeignKey,
    Boolean,
)
from sqlalchemy.sql import func

from app.database import Base


class Job(Base):
    """Job posting model."""

    __tablename__ = "jobs"

    id = Column(String(36), primary_key=True, index=True)

    user_id = Column(
        String(36),
        ForeignKey("users.id"),
        nullable=False,
        index=True,
    )

    # Job Information
    title = Column(
        String(255),
        nullable=False,
        index=True,
    )

    description = Column(
        Text,
        nullable=False,
    )

    requirements = Column(
        JSON,
        default=list,
        nullable=False,
    )

    nice_to_have = Column(
        JSON,
        default=list,
        nullable=False,
    )

    # Job Details
    seniority_level = Column(
        String(50),
        nullable=True,
    )

    department = Column(
        String(255),
        nullable=True,
    )

    location = Column(
        String(255),
        nullable=True,
    )

    job_type = Column(
        String(50),
        nullable=True,
    )

    # Compensation
    salary_min = Column(
        Float,
        nullable=True,
    )

    salary_max = Column(
        Float,
        nullable=True,
    )

    currency = Column(
        String(10),
        default="USD",
        nullable=False,
    )

    # Embeddings
    description_embedding = Column(
        Text,
        nullable=True,
    )

    # Status
    status = Column(
        String(50),
        default="open",
        nullable=False,
    )

    is_active = Column(
        Boolean,
        default=True,
        nullable=False,
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

    def __repr__(self) -> str:
        return (
            f"<Job(id={self.id}, "
            f"title={self.title}, "
            f"status={self.status})>"
        )