"""Job posting management endpoints."""
from app.api.auth import get_authenticated_user
from app.models.user import User
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc
import uuid

from app.database import get_db
from app.schemas.job import JobCreate, JobUpdate, JobResponse, JobListResponse
from app.models.job import Job
from app.middleware.error_handler import NotFoundError, ValidationError

router = APIRouter(tags=["Jobs"])


@router.post("/", response_model=JobResponse, status_code=201)
async def create_job(
    job_data: JobCreate,
    current_user: User = Depends(get_authenticated_user),
    db: Session = Depends(get_db),
):
    """
    Create a new job posting.
    
    Args:
        job_data: Job creation data
        db: Database session
        
    Returns:
        JobResponse: Created job
    """
    new_job = Job(
        id=str(uuid.uuid4()),
        user_id=current_user.id, # TODO: Get from current user
        title=job_data.title,
        description=job_data.description,
        requirements=job_data.requirements,
        nice_to_have=job_data.nice_to_have,
        seniority_level=job_data.seniority_level,
        department=job_data.department,
        location=job_data.location,
        job_type=job_data.job_type,
        salary_min=job_data.salary_min,
        salary_max=job_data.salary_max,
        currency=job_data.currency,
        status="open",
        is_active=True,
    )

    db.add(new_job)
    db.commit()
    db.refresh(new_job)

    return new_job


@router.get("/", response_model=JobListResponse)
async def list_jobs(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    status: str = Query(None),
    is_active: bool = Query(None),
    db: Session = Depends(get_db),
):
    """
    List job postings with pagination.
    """

    query = db.query(Job)

    if status:
        query = query.filter(Job.status == status)

    if is_active is not None:
        query = query.filter(Job.is_active == is_active)

    total = query.count()

    jobs = (
        query
        .order_by(desc(Job.created_at))
        .offset((page - 1) * limit)
        .limit(limit)
        .all()
    )

    return JobListResponse(
        total=total,
        page=page,
        limit=limit,
        jobs=jobs,
    )


@router.get("/{job_id}", response_model=JobResponse)
async def get_job(job_id: str, db: Session = Depends(get_db)):
    """
    Get job by ID.
    
    Args:
        job_id: Job ID
        db: Database session
        
    Returns:
        JobResponse: Job details
        
    Raises:
        NotFoundError: If job not found
    """
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise NotFoundError("Job")

    return job


@router.patch("/{job_id}", response_model=JobResponse)
async def update_job(
    job_id: str,
    job_data: JobUpdate,
    db: Session = Depends(get_db),
):
    """
    Update job posting.
    
    Args:
        job_id: Job ID
        job_data: Update data
        db: Database session
        
    Returns:
        JobResponse: Updated job
        
    Raises:
        NotFoundError: If job not found
    """
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise NotFoundError("Job")

    # Update fields
    update_data = job_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        if value is not None:
            setattr(job, field, value)

    db.commit()
    db.refresh(job)

    return job


@router.delete("/{job_id}", status_code=204)
async def delete_job(job_id: str, db: Session = Depends(get_db)):
    """
    Delete job posting.
    
    Args:
        job_id: Job ID
        db: Database session
        
    Raises:
        NotFoundError: If job not found
    """
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise NotFoundError("Job")

    db.delete(job)
    db.commit()