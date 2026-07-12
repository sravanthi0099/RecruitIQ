"""Resume request/response schemas."""

from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


class ExperienceItem(BaseModel):
    """Work experience item."""
    company: str
    position: str
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    current: bool = False
    description: Optional[str] = None


class EducationItem(BaseModel):
    """Education item."""
    school: str
    degree: str
    field: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None


class ResumeExtraction(BaseModel):
    """Extracted resume data."""
    skills: List[str] = []
    experience: List[ExperienceItem] = []
    education: List[EducationItem] = []
    certifications: List[str] = []
    languages: List[str] = []


class ResumeResponse(BaseModel):
    """Resume response schema."""
    id: str
    candidate_id: str
    file_name: str
    file_url: str
    file_size: Optional[int] = None
    is_parsed: bool
    parse_status: str
    skills: List[str]
    years_of_experience: Optional[float] = None
    education: List[Dict[str, Any]]
    certifications: List[str]
    readability_score: Optional[float] = None
    completeness_score: Optional[float] = None
    created_at: datetime
    parsed_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class ResumeAnalysisResponse(BaseModel):
    """Resume analysis response."""
    resume_id: str
    candidate_id: str
    extraction: ResumeExtraction
    scores: Dict[str, float]
    summary: str