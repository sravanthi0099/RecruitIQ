"""Health check endpoints."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from loguru import logger

from app.database import get_db
from app.config import settings

router = APIRouter(tags=["Health"])


@router.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "environment": settings.ENVIRONMENT,
        "version": settings.APP_VERSION,
    }


@router.get("/health/detailed")
async def detailed_health_check(db: Session = Depends(get_db)):
    """Detailed health check with database verification."""
    health_status = {
        "status": "healthy",
        "environment": settings.ENVIRONMENT,
        "version": settings.APP_VERSION,
        "database": "unknown",
        "timestamp": None,
    }

    try:
        # Test database connection
        result = db.execute(text("SELECT 1"))
        if result:
            health_status["database"] = "connected"
    except Exception as e:
        logger.error(f"Database health check failed: {e}")
        health_status["database"] = "disconnected"
        health_status["status"] = "degraded"

    return health_status


@router.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Welcome to RecruitIQ",
        "version": settings.APP_VERSION,
        "docs": "/docs",
        "redoc": "/redoc",
    }