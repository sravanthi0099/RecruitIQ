"""Candidate-to-job matching endpoints."""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.agent import (
    MatchingRequest,
    MatchingResponse,
)
from app.middleware.error_handler import (
    NotFoundError,
)
from app.models.job import Job
from app.models.candidate import Candidate
from app.services.matching_service import (
    matching_service,
)

router = APIRouter(tags=["Matching"])


@router.post("/find", response_model=MatchingResponse)
async def find_matches(
    request: MatchingRequest,
    db: Session = Depends(get_db),
):
    job = (
        db.query(Job)
        .filter(Job.id == request.job_id)
        .first()
    )

    if not job:
        raise NotFoundError("Job")

    query = db.query(Candidate)

    if request.candidate_ids:
        query = query.filter(
            Candidate.id.in_(
                request.candidate_ids
            )
        )

    candidates = query.all()

    matches = []

    for candidate in candidates:

        candidate_skills = []

        if candidate.extracted_skills:

            if isinstance(
                candidate.extracted_skills,
                dict,
            ):
                candidate_skills = list(
                    candidate.extracted_skills.keys()
                )

            elif isinstance(
                candidate.extracted_skills,
                list,
            ):
                candidate_skills = (
                    candidate.extracted_skills
                )

        skill_score = (
            matching_service.calculate_skill_match_score(
                candidate_skills,
                job.requirements,
            )
        )

        experience_score = (
            matching_service.calculate_experience_match_score(
                candidate.years_of_experience
                or 0
            )
        )

        overall_score = (
            matching_service.calculate_overall_match_score(
                skill_score,
                experience_score,
            )
        )

        if overall_score >= request.min_score:

            matches.append(
                {
                    "candidate_id": candidate.id,
                    "candidate_name":
                    f"{candidate.first_name} "
                    f"{candidate.last_name}",
                    "match_score": round(
                        overall_score * 100,
                        2,
                    ),
                    "explanation": {
                        "skill_score": round(
                            skill_score * 100,
                            2,
                        ),
                        "experience_score": round(
                            experience_score * 100,
                            2,
                        ),
                    },
                    "strengths":
                    candidate_skills,
                    "gaps": [],
                }
            )

    matches = sorted(
        matches,
        key=lambda x: x["match_score"],
        reverse=True,
    )

    return MatchingResponse(
        job_id=request.job_id,
        total_matches=len(matches),
        matches=matches[: request.top_k],
    )


@router.get("/results/{job_id}")
async def get_match_results(
    job_id: str,
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
):
    job = (
        db.query(Job)
        .filter(Job.id == job_id)
        .first()
    )

    if not job:
        raise NotFoundError("Job")

    candidates = db.query(Candidate).all()

    matches = []

    for candidate in candidates:

        candidate_skills = []

        if candidate.extracted_skills:

            if isinstance(candidate.extracted_skills, dict):
                candidate_skills = list(
                    candidate.extracted_skills.keys()
                )

            elif isinstance(candidate.extracted_skills, list):
                candidate_skills = (
                    candidate.extracted_skills
                )

        skill_score = (
            matching_service.calculate_skill_match_score(
                candidate_skills,
                job.requirements,
            )
        )

        experience_score = (
            matching_service.calculate_experience_match_score(
                candidate.years_of_experience
                or 0
            )
        )

        overall_score = (
            matching_service.calculate_overall_match_score(
                skill_score,
                experience_score,
            )
        )

        matches.append(
            {
                "candidate_id": candidate.id,
                "candidate_name":
                f"{candidate.first_name} {candidate.last_name}",
                "match_score": round(
                    overall_score * 100,
                    2,
                ),
                "skill_score": round(
                    skill_score * 100,
                    2,
                ),
                "experience_score": round(
                    experience_score * 100,
                    2,
                ),
                "skills": candidate_skills,
            }
        )

    matches = sorted(
        matches,
        key=lambda x: x["match_score"],
        reverse=True,
    )

    start = (page - 1) * limit
    end = start + limit

    return {
        "job_id": job_id,
        "total_matches": len(matches),
        "matches": matches[start:end],
        "page": page,
        "limit": limit,
    }