from pydantic import BaseModel, ConfigDict, EmailStr, Field
from typing import Optional, List, Dict, Any, Union
from datetime import datetime


class CandidateBase(BaseModel):
    first_name: str = Field(..., min_length=1, max_length=255)
    last_name: str = Field(..., min_length=1, max_length=255)
    email: EmailStr
    phone: Optional[str] = None
    location: Optional[str] = None


class CandidateCreate(CandidateBase):
    pass


class CandidateUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
    location: Optional[str] = None
    status: Optional[str] = None
    notes: Optional[str] = None


class CandidateResponse(CandidateBase):
    id: str
    status: str
    years_of_experience: Optional[float] = None

    extracted_skills: Union[
        List[str],
        Dict[str, Any]
    ]

    education: List[Any]
    match_score: Optional[float] = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )


class CandidateDetailResponse(CandidateResponse):
    resume_url: Optional[str] = None
    notes: Optional[str] = None


class CandidateBulkCreateRequest(BaseModel):
    candidates: List[CandidateCreate] = Field(
        ...,
        min_length=1,
        max_length=100,
    )


class CandidateListResponse(BaseModel):
    total: int
    page: int
    limit: int
    candidates: List[CandidateResponse]