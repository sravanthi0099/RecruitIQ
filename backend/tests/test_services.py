"""Tests for services."""

import pytest
from app.services import resume_service, matching_service, analytics_service


class TestResumeService:
    """Test Resume Service."""

    def test_extract_skills(self):
        """Test skill extraction."""
        text = "Proficient in Python, AWS, and PostgreSQL"
        skills = resume_service.extract_skills(text)
        
        assert "Python" in skills
        assert "AWS" in skills

    def test_extract_experience_years(self):
        """Test experience extraction."""
        text = "10 years of software development experience"
        years = resume_service.extract_experience_years(text)
        
        assert years == 10.0

    def test_calculate_readability_score(self):
        """Test readability scoring."""
        text = "I worked at Google. I built systems. I learned Python."
        score = resume_service.calculate_readability_score(text)
        
        assert 0 <= score <= 100


class TestMatchingService:
    """Test Matching Service."""

    def test_skill_match_score(self):
        """Test skill match scoring."""
        candidate_skills = ["Python", "AWS"]
        required_skills = ["Python", "AWS", "SQL"]
        
        score = matching_service.calculate_skill_match_score(
            candidate_skills,
            required_skills,
        )
        
        assert 0 <= score <= 1
        assert score == pytest.approx(2/3, 0.1)

    def test_experience_match_score(self):
        """Test experience match scoring."""
        score = matching_service.calculate_experience_match_score(
            candidate_years=5,
            min_years=3,
            max_years=10,
        )
        
        assert 0 <= score <= 1
        assert score == 1.0  # Meets requirement

    def test_overall_match_score(self):
        """Test overall match scoring."""
        score = matching_service.calculate_overall_match_score(
            skill_score=0.8,
            experience_score=0.9,
        )
        
        assert 0 <= score <= 1
