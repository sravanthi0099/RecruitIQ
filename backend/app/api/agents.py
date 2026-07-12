"""AI Agent endpoints."""
from app.agents.ai_resume_agent import AIResumeAgent
from app.agents.jd_agent import JDAgent
from app.agents.skill_gap_agent import SkillGapAgent
from app.agents.ai_candidate_ranker import AICandidateRanker
from app.agents.gemini_interview_agent import GeminiInterviewAgent
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.agents.ai_hiring_committee import AIHiringCommittee
from app.agents.multi_llm_evaluator import (
    MultiLLMEvaluator
)
import uuid

from app.models.ai_analysis import (
    AIAnalysis
)
from app.models.interview_response import (
    InterviewResponse
)

from app.schemas.agent import (
    InterviewEvaluationRequest
)
from app.services.email_service import (
    email_service
)
from app.services.email_service import email_service
from app.services.email_templates import EmailTemplates

from app.schemas.agent import (
    SendEmailRequest
)
from app.schemas.agent import InterviewInviteRequest
from app.agents.recruiter_copilot import RecruiterCopilot
from app.database import get_db
from app.api.auth import get_authenticated_user
from app.models.user import User

from app.schemas.agent import (
    ResumeAnalysisRequest,
    ResumeAnalysisResponse,
    MatchingRequest,
    MatchingResponse,
    BiasAuditRequest,
    BiasAuditResponse,
    SalaryEstimationRequest,
    SalaryEstimationResponse,
    InterviewQuestionRequest,
    InterviewQuestionsResponse,
)

from app.middleware.error_handler import NotFoundError

from app.agents.resume_agent import ResumeAgent
from app.agents.matching_agent import MatchingAgent
from app.agents.bias_agent import BiasAgent
from app.agents.salary_agent import SalaryAgent
from app.agents.interview_agent import InterviewAgent

from app.models.candidate import Candidate
from app.models.job import Job

router = APIRouter(tags=["AI Agents"])


@router.post(
    "/resume/analyze",
    response_model=ResumeAnalysisResponse,
)
async def analyze_resume(
    request: ResumeAnalysisRequest,
    current_user: User = Depends(get_authenticated_user),
    db: Session = Depends(get_db),
):
    """
    Analyze resume using Resume Agent.
    """

    agent = ResumeAgent()

    result = await agent.execute(
        {
            "resume_text": request.resume_text,
        }
    )

    return ResumeAnalysisResponse(
        skills=result.get("skills", []),
        experience_years=result.get(
            "experience_years",
            0,
        ),
        education=result.get(
            "education",
            [],
        ),
        summary=result.get(
            "summary",
            "",
        ),
        confidence_score=result.get(
            "confidence_score",
            0.0,
        ),
    )


@router.post(
    "/matching/find",
    response_model=MatchingResponse,
)
async def find_matching_candidates(
    request: MatchingRequest,
    current_user: User = Depends(get_authenticated_user),
    db: Session = Depends(get_db),
):
    """
    Find matching candidates using Matching Agent.
    """

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

    agent = MatchingAgent()

    for candidate in candidates:

        candidate_skills = (
            candidate.extracted_skills
            or []
        )

        result = await agent.execute(
            {
                "candidate_skills":
                candidate_skills,
                "required_skills":
                job.requirements or [],
                "candidate_years":
                candidate.years_of_experience
                or 0,
                "min_years": 0,
                "max_years": 20,
            }
        )

        if (
            result["match_score"]
            >= request.min_score
        ):
            matches.append(
                {
                    "candidate_id":
                    candidate.id,
                    "candidate_name":
                    f"{candidate.first_name} "
                    f"{candidate.last_name}",
                    "match_score":
                    round(
                        result[
                            "match_score"
                        ]
                        * 100,
                        2,
                    ),
                    "explanation":
                    result[
                        "explanation"
                    ],
                    "strengths":
                    result[
                        "strengths"
                    ],
                    "gaps":
                    result["gaps"],
                }
            )

    matches = sorted(
        matches,
        key=lambda x: x[
            "match_score"
        ],
        reverse=True,
    )

    return MatchingResponse(
        job_id=request.job_id,
        total_matches=len(matches),
        matches=matches[
            : request.top_k
        ],
    )


@router.post(
    "/bias/audit",
    response_model=BiasAuditResponse,
)
async def run_bias_audit(
    request: BiasAuditRequest,
    current_user: User = Depends(get_authenticated_user),
    db: Session = Depends(get_db),
):
    """
    Run bias audit using Bias Agent.
    """

    query = db.query(Candidate)

    if request.candidate_ids:
        query = query.filter(
            Candidate.id.in_(
                request.candidate_ids
            )
        )

    candidates = query.all()

    candidate_data = []

    for candidate in candidates:
        candidate_data.append(
            {
                "location":
                candidate.location
                or "",
                "education_school":
                str(
                    candidate.education
                ),
            }
        )

    agent = BiasAgent()

    result = await agent.execute(
        {
            "job_id":
            request.job_id,
            "candidates":
            candidate_data,
        }
    )

    return BiasAuditResponse(
        job_id=request.job_id,
        gender_diversity=result.get(
            "gender_diversity",
            {},
        ),
        college_diversity=result.get(
            "education_diversity",
            {},
        ),
        geographic_diversity=result.get(
            "geographic_diversity",
            {},
        ),
        bias_score=result.get(
            "bias_score",
            0.0,
        ),
        recommendations=result.get(
            "recommendations",
            [],
        ),
    )


@router.post(
    "/salary/estimate",
    response_model=SalaryEstimationResponse,
)
async def estimate_salary(
    request: SalaryEstimationRequest,
    current_user: User = Depends(get_authenticated_user),
):
    """
    Estimate salary using Salary Agent.
    """

    agent = SalaryAgent()

    result = await agent.execute(
        {
            "job_title":
            request.job_title,
            "location":
            request.location,
            "experience_years":
            request.experience_years
            or 0,
            "skills":
            request.skills or [],
        }
    )

    return SalaryEstimationResponse(
        estimated_salary=result[
            "estimated_salary"
        ],
        salary_range=result[
            "salary_range"
        ],
        market_data=result[
            "market_data"
        ],
        currency=result[
            "currency"
        ],
    )


@router.post(
    "/interview/generate-questions",
    response_model=InterviewQuestionsResponse,
)
async def generate_interview_questions(
    request: InterviewQuestionRequest,
    current_user: User = Depends(get_authenticated_user),
    db: Session = Depends(get_db),
):
    """
    Generate interview questions using Interview Agent.
    """

    candidate = (
        db.query(Candidate)
        .filter(
            Candidate.id
            == request.candidate_id
        )
        .first()
    )

    if not candidate:
        raise NotFoundError(
            "Candidate"
        )

    job = (
        db.query(Job)
        .filter(
            Job.id
            == request.job_id
        )
        .first()
    )

    if not job:
        raise NotFoundError(
            "Job"
        )

    candidate_skills = (
        candidate.extracted_skills
        or []
    )

    job_requirements = (
        job.requirements or []
    )

    combined_skills = list(
        set(
            candidate_skills
            + job_requirements
        )
    )

    agent = InterviewAgent()

    result = await agent.execute(
    {
        "candidate_skills": candidate_skills,
        "job_requirements": job_requirements,
        "experience_years":
        candidate.years_of_experience or 0,
        "difficulty":
        request.difficulty,
        "num_questions":
        request.num_questions,
    }
)
    return InterviewQuestionsResponse(
        candidate_id=
        request.candidate_id,
        job_id=request.job_id,
        questions=result[
            "questions"
        ],
    )
@router.post("/full-analysis")
async def full_analysis(
    candidate_id: str,
    job_id: str,
    current_user: User = Depends(get_authenticated_user),
    db: Session = Depends(get_db),
):
    """
    Run complete RecruitIQ AI pipeline.
    """

    candidate = (
        db.query(Candidate)
        .filter(Candidate.id == candidate_id)
        .first()
    )

    if not candidate:
        raise NotFoundError("Candidate")

    job = (
        db.query(Job)
        .filter(Job.id == job_id)
        .first()
    )

    if not job:
        raise NotFoundError("Job")

    resume_text = candidate.resume_text or ""
    job_description = job.description or ""

    # Resume Analysis
    resume_agent = AIResumeAgent()

    resume_result = await resume_agent.execute(
        {
            "resume_text": resume_text
        }
    )

    # JD Analysis
    jd_agent = JDAgent()

    jd_result = await jd_agent.execute(
        {
            "job_description": job_description
        }
    )

    # Skill Gap Analysis
    gap_agent = SkillGapAgent()

    gap_result = await gap_agent.execute(
        {
            "candidate_skills": resume_result.get(
                "skills",
                []
            ),
            "required_skills": jd_result.get(
                "required_skills",
                []
            ),
            "candidate_level": resume_result.get(
                "candidate_level",
                "Junior"
            ),
        }
    )

    # Candidate Ranking
    ranker = AICandidateRanker()

    rank_result = await ranker.execute(
        {
            "candidate_profile": resume_result,
            "job_profile": jd_result,
            "skill_gap_profile": gap_result,
        }
    )

    # Interview Questions
    interview_agent = GeminiInterviewAgent()

    interview_result = await interview_agent.execute(
        {
            "candidate_profile": resume_result,
            "job_profile": jd_result,
            "skill_gap_profile": gap_result,
            "difficulty": "medium",
            "num_questions": 10,
        }
    )

    # -------------------------
    # AI Hiring Committee
    # -------------------------
    multi_llm = MultiLLMEvaluator()

    # Build a clean, human-readable summary instead of dumping the raw
    # Python dict (str(resume_result)) into the prompt. The old approach
    # stuffed the prompt full of extra { } characters, which made Gemini
    # and Cerebras far more likely to echo them back and break the
    # response's JSON extraction -- silently zeroing their scores on
    # every run regardless of candidate quality.
    #
    # This summary also now includes the skill-gap result (matching vs.
    # missing required skills). Without it, the three LLMs were only
    # judging "is this a strong resume in general" -- which let a
    # candidate missing every required skill still score a "Hire" purely
    # on the strength of unrelated experience. Feeding the gap explicitly
    # makes their score reflect fit for *this* job, not general quality.
    matching_skills = gap_result.get("matching_skills", [])
    missing_skills = gap_result.get("missing_skills", [])
    match_score = gap_result.get("match_score", 0)

    candidate_summary = (
        f"Skills: {', '.join(resume_result.get('skills', []) or ['Not specified'])}\n"
        f"Experience: {resume_result.get('experience_years', 0)} years "
        f"({resume_result.get('candidate_level', 'Unknown')} level)\n"
        f"Career Summary: {resume_result.get('career_summary', 'Not available')}\n\n"
        f"Required-skill match for this specific job: {match_score}%\n"
        f"Matching required skills: {', '.join(matching_skills) or 'None'}\n"
        f"Missing required skills: {', '.join(missing_skills) or 'None'}"
    )

    multi_llm_result = await multi_llm.execute(
        {
            "question":
            "Evaluate this candidate's fit for THIS SPECIFIC job. A strong "
            "general resume does not make up for missing required skills -- "
            "weigh the required-skill match/gap below heavily. A candidate "
            "missing most required skills should not score as a Hire, "
            "regardless of how strong their unrelated experience is.",

            "answer":
            candidate_summary,

            "job_role":
            jd_result.get(
                "role",
                ""
            )
        }
    )
    committee_agent = AIHiringCommittee()


    committee_result = await committee_agent.execute(
        {
    "resume_analysis":
    resume_result,

    "job_analysis":
    jd_result,

    "skill_gap_analysis":
    gap_result,

    "candidate_ranking":
    rank_result,

    "multi_llm_evaluation":
    multi_llm_result
}
    )


    decision = committee_result.get(
        "committee_decision",
        "Consider"
    )
    candidate_name = (
        f"{candidate.first_name} "
        f"{candidate.last_name}"
    )

    job_title = job.title

    try:

        if decision in [
            "Strong Hire",
            "Hire"
        ]:

            subject, body = (
                EmailTemplates.shortlist_email(
                    candidate_name,
                    job_title
                )
            )

            await email_service.send_email(
                to_email=candidate.email,
                subject=subject,
                body=body
            )

            print(
                "SHORTLIST EMAIL SENT"
            )

        elif decision == "Reject":

            subject, body = (
                EmailTemplates.rejection_email(
                    candidate_name,
                    job_title
                )
            )

            await email_service.send_email(
                to_email=candidate.email,
                subject=subject,
                body=body
            )

            print(
                "REJECTION EMAIL SENT"
            )

    except Exception as e:

        print(
            "EMAIL FAILED:",
            str(e)
        )
    analysis = AIAnalysis(
        id=str(uuid.uuid4()),
        candidate_id=candidate_id,
        job_id=job_id,
        resume_analysis=resume_result,
        job_analysis=jd_result,
        skill_gap_analysis=gap_result,
        candidate_ranking=rank_result,
        interview_questions=interview_result,
        committee_result=committee_result,
        final_decision=decision
    )

    print("================================")
    print("SAVING AI ANALYSIS")
    print("Candidate:", candidate_id)
    print("Job:", job_id)
    print("================================")

    
    try:

        db.add(analysis)
        db.commit()
        db.refresh(analysis)

        print("AI ANALYSIS SAVED")
        print("Analysis ID:", analysis.id)

    except Exception as e:

        db.rollback()

        print("SAVE FAILED")
        print(str(e))

        raise e

    return {
        "analysis_id": analysis.id,
        "candidate_id": candidate_id,
        "job_id": job_id,
        "resume_analysis": resume_result,
        "job_analysis": jd_result,
        "skill_gap_analysis": gap_result,
        "candidate_ranking": rank_result,
        "interview_questions": interview_result,
        "multi_llm_evaluation": multi_llm_result,
        "committee_result": committee_result,
        "final_decision": decision
    }
@router.get("/analysis/{analysis_id}")
async def get_analysis(
    analysis_id: str,
    current_user: User = Depends(get_authenticated_user),
    db: Session = Depends(get_db)
):

    analysis = (
        db.query(AIAnalysis)
        .filter(
            AIAnalysis.id == analysis_id
        )
        .first()
    )

    if not analysis:
        return {
            "error": "Analysis not found"
        }

    return {
        "analysis_id": analysis.id,
        "candidate_id": analysis.candidate_id,
        "job_id": analysis.job_id,
        "resume_analysis": analysis.resume_analysis,
        "job_analysis": analysis.job_analysis,
        "skill_gap_analysis": analysis.skill_gap_analysis,
        "candidate_ranking": analysis.candidate_ranking,
        "interview_questions": analysis.interview_questions,
        "committee_result": analysis.committee_result,
        "final_decision": analysis.final_decision,
        "created_at": analysis.created_at
    }
@router.post(
    "/interview/evaluate"
)
async def evaluate_answer(
    request: InterviewEvaluationRequest,
    current_user: User = Depends(get_authenticated_user),
    db: Session = Depends(get_db)
):

    evaluator = MultiLLMEvaluator()

    result = await evaluator.execute(
        {
            "question":
            request.question,

            "answer":
            request.answer,

            "job_role":
            "AI ML Engineer"
        }
    )

    record = InterviewResponse(
        id=str(uuid.uuid4()),
        candidate_id=request.candidate_id,
        job_id=request.job_id,
        question=request.question,
        answer=request.answer,
        groq_score=result["groq_score"],
        gemini_score=result["gemini_score"],
        cerebras_score=result["cerebras_score"],
        final_score=result["final_score"],
        recommendation=result["recommendation"]
    )

    db.add(record)

    db.commit()

    return {
        "response_id": record.id,
        **result
    }
@router.post("/email/send")
async def send_candidate_email(
    request: SendEmailRequest,
    current_user: User = Depends(get_authenticated_user),
    db: Session = Depends(get_db)
):

    candidate = (
        db.query(Candidate)
        .filter(
            Candidate.id ==
            request.candidate_id
        )
        .first()
    )

    if not candidate:
        return {
            "error":
            "Candidate not found"
        }

    await email_service.send_email(
        to_email=candidate.email,
        subject=request.subject,
        body=request.body
    )

    return {
        "message":
        "Email sent successfully"
    }

@router.post("/recruiter/copilot")
async def recruiter_copilot(
    question: str,
    current_user: User = Depends(get_authenticated_user),
    db: Session = Depends(get_db)
):

    analyses = db.query(
        AIAnalysis
    ).all()

    context = []

    for analysis in analyses:

        candidate = (
            db.query(Candidate)
            .filter(
                Candidate.id ==
                analysis.candidate_id
            )
            .first()
        )

        context.append(
            {
                "candidate_name":
                f"{candidate.first_name} {candidate.last_name}"
                if candidate else "Unknown",

                "candidate_id":
                analysis.candidate_id,

                "job_id":
                analysis.job_id,

                "decision":
                analysis.final_decision,

                "overall_score":
                analysis.candidate_ranking.get(
                    "overall_score",
                    0
                ),

                "technical_fit":
                analysis.candidate_ranking.get(
                    "technical_fit",
                    0
                ),

                "skill_gap":
                analysis.skill_gap_analysis
            }
        )

        copilot = RecruiterCopilot()

        result = await copilot.execute(
            {
                "question": question,
                "context": context
            }
        )

        return result

@router.post("/interview/invite")
async def invite_candidate_to_interview(
    request: InterviewInviteRequest,
    current_user: User = Depends(get_authenticated_user),
    db: Session = Depends(get_db)
):

    candidate = (
        db.query(Candidate)
        .filter(
            Candidate.id ==
            request.candidate_id
        )
        .first()
    )

    if not candidate:
        return {
            "error":
            "Candidate not found"
        }

    job = (
        db.query(Job)
        .filter(
            Job.id ==
            request.job_id
        )
        .first()
    )

    if not job:
        return {
            "error":
            "Job not found"
        }

    subject, body = (
        EmailTemplates.interview_invite_email(
            candidate_name=
            f"{candidate.first_name} {candidate.last_name}",

            job_title=
            job.title,

            interview_date=
            request.interview_date,

            interview_link=
            request.interview_link
        )
    )

    await email_service.send_email(
        to_email=candidate.email,
        subject=subject,
        body=body
    )

    return {
        "message":
        "Interview invitation sent successfully",

        "candidate":
        candidate.email,

        "job":
        job.title
    }