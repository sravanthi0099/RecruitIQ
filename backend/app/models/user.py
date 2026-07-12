"""User database model."""

import enum

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Enum,
    String,
)
from sqlalchemy.sql import func

from app.database import Base


class UserRole(str, enum.Enum):
    """User role enumeration."""

    ADMIN = "admin"
    RECRUITER = "recruiter"
    HIRING_MANAGER = "hiring_manager"
    VIEWER = "viewer"


class User(Base):
    """User model."""

    __tablename__ = "users"

    id = Column(String(36), primary_key=True, index=True)

    email = Column(
        String(255),
        unique=True,
        index=True,
        nullable=False,
    )

    full_name = Column(
        String(255),
        nullable=True,
    )

    hashed_password = Column(
        String(255),
        nullable=False,
    )

    role = Column(
        Enum(UserRole),
        default=UserRole.RECRUITER,
        nullable=False,
    )

    is_active = Column(
        Boolean,
        default=True,
        nullable=False,
    )

    is_verified = Column(
        Boolean,
        default=False,
        nullable=False,
    )

    google_id = Column(
        String(255),
        unique=True,
        nullable=True,
        index=True,
    )

    oauth_provider = Column(
        String(50),
        nullable=True,
    )

    created_at = Column(
        DateTime,
        server_default=func.now(),
        nullable=False,
    )

    updated_at = Column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    last_login = Column(
        DateTime,
        nullable=True,
    )

    def __repr__(self) -> str:
        return (
            f"<User(id={self.id}, "
            f"email={self.email}, "
            f"role={self.role})>"
        )