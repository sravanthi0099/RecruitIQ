"""Candidate management endpoints."""

import os
import json
import uuid

from fastapi import (
    APIRouter,
    Depends,
    File,
    UploadFile,
    Query,
    HTTPException,
)

from sqlalchemy.orm import Session

from app.database import get_db
from app.api.auth import get_authenticated_user

from app.models.user import User
from app.models.candidate import Candidate
from app.models.resume import Resume

from app.schemas.candidate import (
    CandidateCreate,
    CandidateUpdate,
    CandidateResponse,
    CandidateListResponse,
    CandidateDetailResponse,
)

from app.services.resume_parser import (
    extract_text_from_pdf,
    extract_text_from_docx,
)

from app.services.embedding_service import (
    generate_embedding,
)

from app.services.resume_service import (
    resume_service,
)

from app.middleware.error_handler import (
    NotFoundError,
    ValidationError,
)

router = APIRouter(tags=["Candidates"])


@router.post("/", response_model=CandidateResponse, status_code=201)
async def create_candidate(
    candidate_data: CandidateCreate,
    current_user: User = Depends(get_authenticated_user),
    db: Session = Depends(get_db),
):
    existing = (
        db.query(Candidate)
        .filter(Candidate.email == candidate_data.email)
        .first()
    )

    if existing:
        raise ValidationError(
            "Candidate with this email already exists"
        )

    new_candidate = Candidate(
        id=str(uuid.uuid4()),
        user_id=current_user.id,
        first_name=candidate_data.first_name,
        last_name=candidate_data.last_name,
        email=candidate_data.email,
        phone=candidate_data.phone,
        location=candidate_data.location,
        status="new",
    )

    db.add(new_candidate)
    db.commit()
    db.refresh(new_candidate)

    return new_candidate


@router.get("/", response_model=CandidateListResponse)
async def list_candidates(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    status: str = Query(None),
    db: Session = Depends(get_db),
):
    query = db.query(Candidate)

    if status:
        query = query.filter(
            Candidate.status == status
        )

    total = query.count()

    candidates = (
        query.offset((page - 1) * limit)
        .limit(limit)
        .all()
    )

    return CandidateListResponse(
        total=total,
        page=page,
        limit=limit,
        candidates=candidates,
    )


@router.get(
    "/{candidate_id}",
    response_model=CandidateDetailResponse,
)
async def get_candidate(
    candidate_id: str,
    db: Session = Depends(get_db),
):
    candidate = (
        db.query(Candidate)
        .filter(Candidate.id == candidate_id)
        .first()
    )

    if not candidate:
        raise NotFoundError("Candidate")

    return candidate


@router.patch(
    "/{candidate_id}",
    response_model=CandidateResponse,
)
async def update_candidate(
    candidate_id: str,
    candidate_data: CandidateUpdate,
    db: Session = Depends(get_db),
):
    candidate = (
        db.query(Candidate)
        .filter(Candidate.id == candidate_id)
        .first()
    )

    if not candidate:
        raise NotFoundError("Candidate")

    update_data = candidate_data.model_dump(
        exclude_unset=True
    )

    for field, value in update_data.items():
        setattr(candidate, field, value)

    db.commit()
    db.refresh(candidate)

    return candidate


@router.delete("/{candidate_id}", status_code=204)
async def delete_candidate(
    candidate_id: str,
    db: Session = Depends(get_db),
):
    candidate = (
        db.query(Candidate)
        .filter(Candidate.id == candidate_id)
        .first()
    )

    if not candidate:
        raise NotFoundError("Candidate")

    db.delete(candidate)
    db.commit()


@router.post("/{candidate_id}/upload-resume")
async def upload_resume(
    candidate_id: str,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    candidate = (
        db.query(Candidate)
        .filter(Candidate.id == candidate_id)
        .first()
    )

    if not candidate:
        raise NotFoundError("Candidate")

    if not file.filename.lower().endswith((".pdf", ".docx")):
        raise HTTPException(
            status_code=400,
            detail="Only PDF and DOCX files are supported",
        )

    upload_dir = "uploads/resumes"

    os.makedirs(
        upload_dir,
        exist_ok=True,
    )

    safe_filename = (
        f"{candidate_id}_{file.filename}"
    )

    file_path = os.path.join(
        upload_dir,
        safe_filename,
    )

    contents = await file.read()

    with open(file_path, "wb") as buffer:
        buffer.write(contents)

    try:
        if file.filename.lower().endswith(".pdf"):
            resume_text = extract_text_from_pdf(file_path)
        elif file.filename.lower().endswith(".docx"):
            resume_text = extract_text_from_docx(file_path)
        else:
            raise HTTPException(
                status_code=400,
                detail="Only PDF and DOCX files are supported",
            )

        if not resume_text:
            raise HTTPException(
                status_code=400,
                detail="Unable to extract text from resume",
            )

        skills = resume_service.extract_skills(
            resume_text
        )

        years = (
            resume_service.extract_experience_years(
                resume_text
            )
        )

        embedding = generate_embedding(
            resume_text
        )

        candidate.resume_url = file_path
        candidate.resume_text = resume_text
        candidate.resume_embedding = json.dumps(
            embedding
        )
        candidate.extracted_skills = skills
        candidate.years_of_experience = years

        resume_record = Resume(
            id=str(uuid.uuid4()),
            candidate_id=candidate.id,
            file_name=file.filename,
            file_url=file_path,
            file_size=len(contents),
            raw_text=resume_text,
            embedding=json.dumps(
                embedding
            ),
            skills=skills,
            education=[],
            experience=[],
            is_parsed=True,
            parse_status="completed",
        )

        db.add(resume_record)

        db.commit()

        db.refresh(candidate)

        return {
            "message": "Resume processed successfully",
            "candidate_id": candidate_id,
            "filename": file.filename,
            "skills": skills,
            "years_of_experience": years,
            "text_length": len(resume_text),
            "embedding_dimension": len(
                embedding
            ),
        }

    except Exception as e:
        db.rollback()

        raise HTTPException(
            status_code=500,
            detail=f"Resume processing failed: {str(e)}",
        )