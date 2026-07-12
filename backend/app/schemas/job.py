"""Job request/response schemas."""

from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


class JobBase(BaseModel):
    """Base job schema."""
    title: str = Field(..., min_length=1, max_length=255)
    description: str = Field(..., min_length=10)
    requirements: List[str] = Field(default=[], max_items=50)
    nice_to_have: List[str] = Field(default=[], max_items=50)


class JobCreate(JobBase):
    """Job creation schema."""
    seniority_level: Optional[str] = None
    department: Optional[str] = None
    location: Optional[str] = None
    job_type: Optional[str] = None
    salary_min: Optional[float] = None
    salary_max: Optional[float] = None
    currency: str = "USD"


class JobUpdate(BaseModel):
    """Job update schema."""
    title: Optional[str] = None
    description: Optional[str] = None
    requirements: Optional[List[str]] = None
    nice_to_have: Optional[List[str]] = None
    status: Optional[str] = None
    is_active: Optional[bool] = None


class JobResponse(JobBase):
    """Job response schema."""
    id: str
    status: str
    is_active: bool
    seniority_level: Optional[str] = None
    department: Optional[str] = None
    location: Optional[str] = None
    job_type: Optional[str] = None
    salary_min: Optional[float] = None
    salary_max: Optional[float] = None
    currency: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class JobListResponse(BaseModel):
    """Paginated job list response."""
    total: int
    page: int
    limit: int
    jobs: List[JobResponse]