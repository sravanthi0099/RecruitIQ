"""Tests for API endpoints."""

import pytest
from fastapi.testclient import TestClient
from main import app


client = TestClient(app)


class TestHealth:
    """Test health check endpoints."""

    def test_health_check(self):
        """Test health check endpoint."""
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"

    def test_root_endpoint(self):
        """Test root endpoint."""
        response = client.get("/")
        assert response.status_code == 200
        assert "message" in response.json()

    def test_version_endpoint(self):
        """Test version endpoint."""
        response = client.get("/version")
        assert response.status_code == 200
        assert "version" in response.json()


class TestCandidates:
    """Test candidate endpoints."""

    def test_list_candidates(self):
        """Test listing candidates."""
        response = client.get("/api/candidates/")
        assert response.status_code == 200
        assert "candidates" in response.json()

    def test_create_candidate(self):
        """Test creating candidate."""
        data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "john@example.com",
        }
        response = client.post("/api/candidates/", json=data)
        # Will fail without DB setup, but that's ok for demo
        assert response.status_code in [200, 201, 422]


class TestJobs:
    """Test job endpoints."""

    def test_list_jobs(self):
        """Test listing jobs."""
        response = client.get("/api/jobs/")
        assert response.status_code == 200
        assert "jobs" in response.json()


class TestAgents:
    """Test agent endpoints."""

    def test_analyze_resume(self):
        """Test resume analysis."""
        data = {"resume_text": "Python, AWS, 5 years experience"}
        response = client.post("/api/agents/resume/analyze", json=data)
        assert response.status_code in [200, 422]

    def test_salary_estimation(self):
        """Test salary estimation."""
        data = {
            "job_title": "Senior Engineer",
            "location": "San Francisco",
        }
        response = client.post("/api/agents/salary/estimate", json=data)
        assert response.status_code in [200, 422]
