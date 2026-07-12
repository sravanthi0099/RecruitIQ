from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.candidate import Candidate
from app.models.job import Job

from app.agents.ai_resume_agent import AIResumeAgent
from app.agents.jd_agent import JDAgent
from app.agents.skill_gap_agent import SkillGapAgent
from app.agents.ai_candidate_ranker import AICandidateRanker

router = APIRouter(tags=["Recruiter"])


@router.get("/shortlist/{job_id}")
async def shortlist_candidates(
    job_id: str,
    db: Session = Depends(get_db)
):
    """
    Recruiter candidate shortlisting endpoint.
    """

    job = (
        db.query(Job)
        .filter(Job.id == job_id)
        .first()
    )

    if not job:
        return {
            "error": "Job not found"
        }

    candidates = db.query(Candidate).all()

    if not candidates:
        return {
            "job_id": job_id,
            "total_candidates": 0,
            "top_candidates": []
        }

    jd_agent = JDAgent()
    gap_agent = SkillGapAgent()
    ranker = AICandidateRanker()

    jd_result = await jd_agent.execute(
        {
            "job_description":
            job.description or ""
        }
    )

    leaderboard = []

    for candidate in candidates:

        try:

            resume_agent = AIResumeAgent()

            resume_result = await resume_agent.execute(
                {
                    "resume_text":
                    candidate.resume_text or ""
                }
            )

            gap_result = await gap_agent.execute(
                {
                    "candidate_skills":
                    resume_result.get(
                        "skills",
                        []
                    ),

                    "required_skills":
                    jd_result.get(
                        "required_skills",
                        []
                    ),

                    "candidate_level":
                    resume_result.get(
                        "candidate_level",
                        "Junior"
                    )
                }
            )

            rank_result = await ranker.execute(
                {
                    "candidate_profile":
                    resume_result,

                    "job_profile":
                    jd_result,

                    "skill_gap_profile":
                    gap_result
                }
            )

            leaderboard.append(
                {
                    "candidate_id":
                    candidate.id,

                    "candidate_name":
                    f"{candidate.first_name} {candidate.last_name}",

                    "email":
                    candidate.email,

                    "match_score":
                    gap_result.get(
                        "match_score",
                        0
                    ),

                    "overall_score":
                    rank_result.get(
                        "overall_score",
                        0
                    ),

                    "recommendation":
                    rank_result.get(
                        "recommendation",
                        "Consider"
                    ),

                    "technical_fit":
                    rank_result.get(
                        "technical_fit",
                        0
                    ),

                    "growth_potential":
                    rank_result.get(
                        "growth_potential",
                        0
                    ),

                    "skill_gaps":
                    gap_result.get(
                        "missing_skills",
                        []
                    ),

                    "matching_skills":
                    gap_result.get(
                        "matching_skills",
                        []
                    )
                }
            )

        except Exception as e:

            print("\n")
            print("=" * 50)
            print("CANDIDATE FAILED")
            print("ID:", candidate.id)
            print("NAME:", candidate.first_name)
            print("EMAIL:", candidate.email)
            print("RESUME:", candidate.resume_text)
            print("ERROR:", str(e))
            print("=" * 50)
            print("\n")

    leaderboard = sorted(
        leaderboard,
        key=lambda x: x["overall_score"],
        reverse=True
    )

    return {
        "job_id": job_id,
        "job_title": job.title,
        "total_candidates": len(candidates),
        "ranked_candidates": len(leaderboard),
        "top_candidates": leaderboard[:10]
    }

