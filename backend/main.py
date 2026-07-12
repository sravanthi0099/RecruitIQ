"""RecruitIQ FastAPI Application Entry Point."""

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
from loguru import logger
from slowapi.errors import RateLimitExceeded
from slowapi import _rate_limit_exceeded_handler
from slowapi.middleware import SlowAPIMiddleware

from app.config import settings
from app.rate_limiter import limiter
from app.middleware.error_handler import global_exception_handler
from app.middleware.logging import LoggingMiddleware
from app.database import engine, Base, init_db
from app.api import (
    candidates,
    jobs,
    matching,
    analytics,
    agents,
    auth,
    health,
    recruiter,
    interview,
)

# Configure logging
logger.remove()  # Remove default handler
logger.add(
    "logs/recruitiq.log",
    rotation="500 MB",
    retention="30 days",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
    level=settings.LOG_LEVEL,
)

# Suppress uvicorn access logs in production
if settings.ENVIRONMENT == "production":
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup and shutdown events."""
    # Startup
    logger.info(f"RecruitIQ {settings.APP_VERSION} starting up...")
    logger.info(f"Environment: {settings.ENVIRONMENT}")
    
    try:
        init_db()
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Database initialization failed: {e}", exc_info=True)
        raise

    yield

    # Shutdown
    logger.info("RecruitIQ shutting down...")


# Create FastAPI application
app = FastAPI(
    title=settings.APP_NAME,
    description="Cloud-Native AI Hiring Intelligence Platform",
    version=settings.APP_VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan,
)

# Add custom middleware
app.add_middleware(LoggingMiddleware)

# Rate limiting -- global default (see app/rate_limiter.py); protects
# every route, including the LLM-calling ones, from being hammered.
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=settings.CORS_CREDENTIALS,
    allow_methods=settings.CORS_METHODS,
    allow_headers=settings.CORS_HEADERS,
)

# Trusted host middleware
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=settings.ALLOWED_HOSTS,
)

# Add exception handler
app.add_exception_handler(Exception, global_exception_handler)


# Include routers
app.include_router(health.router, tags=["Health"])
app.include_router(auth.router, prefix=f"{settings.API_PREFIX}/auth", tags=["Authentication"])
app.include_router(candidates.router, prefix=f"{settings.API_PREFIX}/candidates", tags=["Candidates"])
app.include_router(jobs.router, prefix=f"{settings.API_PREFIX}/jobs", tags=["Jobs"])
app.include_router(matching.router, prefix=f"{settings.API_PREFIX}/matching", tags=["Matching"])
app.include_router(analytics.router, prefix=f"{settings.API_PREFIX}/analytics", tags=["Analytics"])
app.include_router(agents.router, prefix=f"{settings.API_PREFIX}/agents", tags=["AI Agents"])
app.include_router(recruiter.router, prefix=f"{settings.API_PREFIX}/recruiter", tags=["Recruiter"])
app.include_router(
    interview.router
)




# Root endpoint
@app.get("/")
async def root():
    """Root endpoint - API information."""
    return {
        "message": "Welcome to RecruitIQ",
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "environment": settings.ENVIRONMENT,
        "documentation": {
            "swagger": "/docs",
            "redoc": "/redoc",
            "openapi": "/openapi.json",
        },
    }


@app.get("/version")
async def version():
    """Get API version."""
    return {
        "version": settings.APP_VERSION,
        "app_name": settings.APP_NAME,
    }


@app.get("/config")
async def config():
    """Get non-sensitive configuration."""
    return {
        "environment": settings.ENVIRONMENT,
        "debug": settings.DEBUG,
        "database_url": settings.DATABASE_URL.split("://")[0] + "://***",
        "cors_origins": settings.CORS_ORIGINS,
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host=settings.SERVER_HOST,
        port=settings.SERVER_PORT,
        reload=settings.ENVIRONMENT == "development",
        log_level=settings.LOG_LEVEL.lower(),
    )
