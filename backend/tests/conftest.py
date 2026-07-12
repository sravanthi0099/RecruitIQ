"""Test configuration and fixtures."""

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base, get_db
from app.config import Settings


@pytest.fixture(scope="session")
def test_settings():
    """Provide test settings."""
    settings = Settings(
        ENVIRONMENT="test",
        DATABASE_URL="sqlite:///:memory:",
        DEBUG=True,
    )
    return settings


@pytest.fixture(scope="session")
def test_db():
    """Create test database."""
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
    )
    
    Base.metadata.create_all(bind=engine)
    
    TestingSessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine,
    )
    
    yield TestingSessionLocal
    
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def db_session(test_db):
    """Provide database session."""
    session = test_db()
    try:
        yield session
    finally:
        session.close()
