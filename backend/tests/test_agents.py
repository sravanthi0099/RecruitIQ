"""Tests for AI agents."""

import pytest
import asyncio
from app.agents import (
    ResumeAgent,
    MatchingAgent,
    BiasAgent,
    SalaryAgent,
    EmailAgent,
    InterviewAgent,
)


class TestResumeAgent:
    """Test Resume Agent."""

    @pytest.mark.asyncio
    async def test_resume_analysis(self):
        """Test resume analysis."""
        agent = ResumeAgent()
        result = await agent.execute({
            "resume_text": "Python, AWS, 8 years experience at Google and Amazon"
        })
        
        assert result["skills"]
        assert result["experience_years"] == 8.0

    @pytest.mark.asyncio
    async def test_resume_analysis_empty(self):
        """Test resume analysis with empty text."""
        agent = ResumeAgent()
        with pytest.raises(ValueError):
            await agent.execute({"resume_text": ""})


class TestMatchingAgent:
    """Test Matching Agent."""

    @pytest.mark.asyncio
    async def test_job_matching(self):
        """Test job matching."""
        agent = MatchingAgent()
        result = await agent.execute({
            "candidate_skills": ["Python", "AWS"],
            "required_skills": ["Python", "AWS", "SQL"],
            "candidate_years": 5,
            "min_years": 3,
        })
        
        assert "match_score" in result
        assert "strengths" in result
        assert "gaps" in result


class TestBiasAgent:
    """Test Bias Agent."""

    @pytest.mark.asyncio
    async def test_bias_analysis(self):
        """Test bias analysis."""
        agent = BiasAgent()
        candidates = [
            {"gender": "male", "location": "New York"},
            {"gender": "female", "location": "San Francisco"},
        ]
        result = await agent.execute({"candidates": candidates})
        
        assert "bias_score" in result
        assert "recommendations" in result


class TestSalaryAgent:
    """Test Salary Agent."""

    @pytest.mark.asyncio
    async def test_salary_estimation(self):
        """Test salary estimation."""
        agent = SalaryAgent()
        result = await agent.execute({
            "job_title": "Senior Software Engineer",
            "location": "San Francisco",
            "experience_years": 7,
        })
        
        assert "estimated_salary" in result
        assert "salary_range" in result


class TestEmailAgent:
    """Test Email Agent."""

    @pytest.mark.asyncio
    async def test_email_generation(self):
        """Test email generation."""
        agent = EmailAgent()
        result = await agent.execute({
            "candidate_name": "John Doe",
            "job_title": "Software Engineer",
            "email_type": "initial_outreach",
            "company_name": "TechCorp",
        })
        
        assert "subject" in result
        assert "body" in result


class TestInterviewAgent:
    """Test Interview Agent."""

    @pytest.mark.asyncio
    async def test_question_generation(self):
        """Test interview question generation."""
        agent = InterviewAgent()
        result = await agent.execute({
            "skills": ["Python", "AWS"],
            "difficulty": "medium",
            "num_questions": 5,
        })
        
        assert "questions" in result
        assert len(result["questions"]) <= 5
