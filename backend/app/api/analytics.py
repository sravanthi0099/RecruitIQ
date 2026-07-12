"""Analytics and reporting endpoints."""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.agent import BiasAuditResponse
from app.services.analytics_service import analytics_service
from app.models.candidate import Candidate
from app.models.ai_analysis import AIAnalysis
from collections import Counter

router = APIRouter(tags=["Analytics"])


@router.get("/funnel")
async def get_hiring_funnel(
    job_id: str = Query(None),
    db: Session = Depends(get_db),
):
    """
    Get real hiring funnel metrics from database.
    """

    funnel_metrics = analytics_service.calculate_funnel_metrics(db)

    time_to_hire = analytics_service.calculate_time_to_hire(db)

    offer_acceptance_rate = (
        analytics_service.calculate_offer_acceptance_rate(db)
    )

    return {
        "job_id": job_id,
        "total_candidates": funnel_metrics["total"],
        "statuses": funnel_metrics["statuses"],
        "conversion_rates": funnel_metrics["conversion_rates"],
        "average_time_to_hire_days": round(
            time_to_hire,
            2,
        ),
        "offer_acceptance_rate": round(
            offer_acceptance_rate * 100,
            2,
        ),
    }


@router.get(
    "/bias-audit",
    response_model=BiasAuditResponse,
)
async def get_bias_audit(
    job_id: str = Query(None),
    db: Session = Depends(get_db),
):
    """
    Basic bias audit from actual candidate data.
    """

    candidates = (
        db.query(Candidate)
        .all()
    )

    location_counts = {}

    for candidate in candidates:

        location = (
            candidate.location
            or "Unknown"
        )

        location_counts[
            location
        ] = (
            location_counts.get(
                location,
                0,
            )
            + 1
        )

    total = max(
        len(candidates),
        1,
    )

    geographic_diversity = {}

    for location, count in (
        location_counts.items()
    ):
        geographic_diversity[
            location
        ] = round(
            count / total,
            2,
        )

    return BiasAuditResponse(
        job_id=job_id or "all",
        gender_diversity={},
        college_diversity={},
        geographic_diversity=
        geographic_diversity,
        bias_score=0.0,
        recommendations=[
            "Gender diversity data not available",
            "Education diversity data not available",
            "Consider storing diversity attributes for advanced auditing",
        ],
    )


@router.get("/salary")
async def get_salary_intelligence(
    job_title: str = Query(None),
    location: str = Query(None),
):
    """
    Salary intelligence endpoint.
    Temporary implementation until Gemini + market APIs are integrated.
    """

    experience_factor = 1.0

    base_salary = 800000

    if (
        job_title
        and "ai"
        in job_title.lower()
    ):
        base_salary = 1200000

    elif (
        job_title
        and "data"
        in job_title.lower()
    ):
        base_salary = 1000000

    elif (
        job_title
        and "backend"
        in job_title.lower()
    ):
        base_salary = 900000

    return {
        "job_title": job_title,
        "location": location,
        "currency": "INR",
        "market_salary": {
            "min": int(
                base_salary * 0.8
            ),
            "max": int(
                base_salary * 1.4
            ),
            "average": int(
                base_salary
            ),
        },
        "percentiles": {
            "p25": int(
                base_salary * 0.85
            ),
            "p50": int(
                base_salary
            ),
            "p75": int(
                base_salary * 1.25
            ),
        },
    }

@router.get("/recruiter-dashboard")
async def recruiter_dashboard(
    db: Session = Depends(get_db)
):

    analyses = db.query(
        AIAnalysis
    ).all()

    total_candidates = len(
        analyses
    )

    strong_hire = 0
    hire = 0
    consider = 0
    reject = 0

    top_candidates = []

    for analysis in analyses:

        decision = (
            analysis.final_decision
            or ""
        )

        if decision == "Strong Hire":
            strong_hire += 1

        elif decision == "Hire":
            hire += 1

        elif decision == "Consider":
            consider += 1

        elif decision == "Reject":
            reject += 1

        ranking = (
            analysis.candidate_ranking
            or {}
        )

        top_candidates.append(
            {
                "candidate_id":
                analysis.candidate_id,

                "score":
                ranking.get(
                    "overall_score",
                    0
                ),

                "decision":
                decision
            }
        )

    top_candidates = sorted(
        top_candidates,
        key=lambda x: x["score"],
        reverse=True
    )

    return {
        "total_candidates":
        total_candidates,

        "strong_hire":
        strong_hire,

        "hire":
        hire,

        "consider":
        consider,

        "reject":
        reject,

        "top_candidates":
        top_candidates[:10]
    }

@router.get("/skill-gap-analytics")
async def skill_gap_analytics(
    db: Session = Depends(get_db)
):

    analyses = db.query(
        AIAnalysis
    ).all()

    missing_skills = []

    for analysis in analyses:

        gap_data = (
            analysis.skill_gap_analysis
            or {}
        )

        skills = gap_data.get(
            "missing_skills",
            []
        )

        missing_skills.extend(
            skills
        )

    counter = Counter(
        missing_skills
    )

    return {
        "total_missing_skills":
        len(missing_skills),

        "top_skill_gaps":
        counter.most_common(10)
    }

@router.get("/hiring-funnel")
async def hiring_funnel(
    db: Session = Depends(get_db)
):

    analyses = db.query(
        AIAnalysis
    ).all()

    total_candidates = len(
        analyses
    )

    strong_hire = 0
    hire = 0
    consider = 0
    reject = 0

    for analysis in analyses:

        decision = (
            analysis.final_decision
            or ""
        )

        if decision == "Strong Hire":
            strong_hire += 1

        elif decision == "Hire":
            hire += 1

        elif decision == "Consider":
            consider += 1

        elif decision == "Reject":
            reject += 1

    shortlisted = (
        strong_hire +
        hire
    )

    return {
        "total_candidates":
        total_candidates,

        "shortlisted":
        shortlisted,

        "strong_hire":
        strong_hire,

        "hire":
        hire,

        "consider":
        consider,

        "reject":
        reject
    }