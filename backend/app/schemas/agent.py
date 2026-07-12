"""Agent request/response schemas."""

from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


class AgentResultBase(BaseModel):
    """Base agent result schema."""
    agent_type: str
    analysis_result: Dict[str, Any]
    recommendations: List[str] = []


class ResumeAnalysisRequest(BaseModel):
    """Resume analysis request."""
    resume_text: str = Field(..., min_length=10)
    candidate_id: Optional[str] = None


class ResumeAnalysisResponse(BaseModel):
    """Resume analysis response."""
    skills: List[str]
    experience_years: float
    education: List[Dict[str, Any]]
    summary: str
    confidence_score: float


class MatchingRequest(BaseModel):
    """Job-candidate matching request."""
    job_id: str
    candidate_ids: Optional[List[str]] = None
    top_k: int = Field(default=10, ge=1, le=100)
    min_score: float = Field(default=0.5, ge=0.0, le=1.0)


class MatchResult(BaseModel):
    """Single match result."""
    candidate_id: str
    candidate_name: str
    match_score: float
    explanation: Dict[str, Any]
    strengths: List[str]
    gaps: List[str]


class MatchingResponse(BaseModel):
    """Job-candidate matching response."""
    job_id: str
    total_matches: int
    matches: List[MatchResult]


class BiasAuditRequest(BaseModel):
    """Bias audit request."""
    job_id: str
    candidate_ids: Optional[List[str]] = None


class BiasAuditResponse(BaseModel):
    """Bias audit response."""
    job_id: str
    gender_diversity: Dict[str, float]
    college_diversity: Dict[str, float]
    geographic_diversity: Dict[str, float]
    bias_score: float
    recommendations: List[str]


class SalaryEstimationRequest(BaseModel):
    """Salary estimation request."""
    job_title: str
    location: str
    experience_years: Optional[float] = None
    skills: Optional[List[str]] = None


class SalaryEstimationResponse(BaseModel):
    """Salary estimation response."""
    estimated_salary: float
    salary_range: Dict[str, float]
    market_data: Dict[str, Any]
    currency: str


class InterviewQuestionRequest(BaseModel):
    """Interview question generation request."""
    candidate_id: str
    job_id: str
    difficulty: str = Field(default="medium", pattern="^(easy|medium|hard)$")
    num_questions: int = Field(default=5, ge=1, le=20)


class InterviewQuestion(BaseModel):
    """Generated interview question."""
    question: str
    topic: str
    difficulty: str
    suggested_answer: Optional[str] = None


class InterviewQuestionsResponse(BaseModel):
    """Interview questions response."""
    candidate_id: str
    job_id: str
    questions: List[InterviewQuestion]


class AgentResultResponse(BaseModel):
    """Agent result response."""
    id: str
    candidate_id: str
    agent_type: str
    status: str
    analysis_result: Dict[str, Any]
    confidence_score: Optional[float] = None
    created_at: datetime
    executed_at: Optional[datetime] = None

    class Config:
        from_attributes = True

from pydantic import BaseModel


class InterviewEvaluationRequest(
    BaseModel
):
    candidate_id: str
    job_id: str
    question: str
    answer: str
class SendEmailRequest(
    BaseModel
):
    candidate_id: str
    subject: str
    body: str

class InterviewInviteRequest(
    BaseModel
):

    candidate_id: str

    job_id: str

    interview_date: str

    interview_link: str

