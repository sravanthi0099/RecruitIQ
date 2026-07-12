# RecruitIQ – Cloud-Native AI Hiring Intelligence Platform

A production-grade AI-powered recruitment system with microservices architecture, multi-agent evaluation pipeline, and advanced analytics.

## Overview

**Problem Statement**: Recruitment is time-consuming, biased, and lacks transparency. RecruitIQ automates candidate evaluation while maintaining explainability and fairness.

## Architecture

             


## Key Features

- **AI-Powered Resume Screening**: Multi-agent system for intelligent candidate evaluation
- **Semantic Matching**: Transformer embeddings with vector search for candidate-job alignment
- **Bias Auditing**: Detect and report hiring bias (gender, college, region)
- **Salary Intelligence**: Market-based salary estimation and negotiation insights
- **Explainable Hiring**: Transparent scoring with detailed reasoning
- **Recruiter Analytics**: Funnel analysis, time-to-hire, acceptance rates
- **Interview Copilot**: AI-generated candidate-specific interview questions
- **Production-Ready**: Full CI/CD, security hardening, monitoring

## Tech Stack

### Frontend
- React + TypeScript
- Vite
- TailwindCSS
- ShadCN UI

### Backend
- FastAPI (Python 3.12+)
- PostgreSQL
- Redis
- pgvector for semantic search

### AI/ML
- LangChain
- Sentence Transformers
- spaCy
- pdfplumber

### DevOps
- Docker & Docker Compose
- Kubernetes (optional)
- AWS (S3, ECS, RDS, CloudFront)
- GitHub Actions (CI/CD)

### Monitoring
- Prometheus
- Grafana
- ELK Stack (ElasticSearch, Logstash, Kibana)

## Quick Start

### Prerequisites
- Docker & Docker Compose
- Python 3.12+
- Node.js 18+
- PostgreSQL 15+

### Development Setup

```bash
# Clone repository
git clone https://github.com/sravanthi0099/RecruitIQ.git
cd RecruitIQ

# Start services with Docker Compose
docker compose up -d

# Frontend runs on http://localhost:3000
# Backend API on http://localhost:8000
# Swagger docs on http://localhost:8000/docs


Manual Setup

# Backend
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload

# Frontend (new terminal)
cd frontend
npm install
npm run dev


API Documentation
Full API documentation available at /docs (Swagger UI) or /redoc after starting the server.

Key Endpoints
Candidates

POST /api/candidates - Create candidate
GET /api/candidates/{id} - Get candidate
POST /api/candidates/{id}/analyze - Analyze resume
Jobs

POST /api/jobs - Create job posting
GET /api/jobs - List jobs
Matching

POST /api/match - Find matching candidates
GET /api/match/results/{job_id} - Get match results
Analytics

GET /api/analytics/funnel - Hiring funnel metrics
GET /api/analytics/bias-audit - Bias analysis
GET /api/analytics/salary - Salary intelligence
AI Agents

POST /api/agents/resume/analyze - Resume analysis
POST /api/agents/bias/audit - Bias detection
POST /api/agents/salary/estimate - Salary estimation
POST /api/agents/interview/generate-questions - Interview questions



Features Breakdown
Phase 1: Microservice Architecture
✅ Separated concerns: Auth, Candidates, Analytics services ✅ API Gateway pattern ✅ Independent scaling

Phase 2: Modern Tech Stack
✅ React + TypeScript frontend ✅ FastAPI backend ✅ PostgreSQL database

Phase 3: Resume Processing
✅ PDF parsing with pdfplumber ✅ NLP with spaCy ✅ Semantic embeddings with Sentence Transformers ✅ Vector search with pgvector

Phase 4: AI Agent System
✅ Resume Agent ✅ Matching Agent ✅ Bias Audit Agent ✅ Salary Estimation Agent ✅ Email Agent ✅ Interview Agent ✅ Agent Orchestrator

Phase 5: Authentication & Authorization
✅ OAuth 2.0 with Google ✅ JWT tokens ✅ Role-Based Access Control (Admin, Recruiter, Hiring Manager) ✅ Secure password hashing

Phase 6: Production Logging
✅ Structured logging with Loguru ✅ ELK Stack integration ✅ Trace IDs for request tracking

Phase 7: Error Handling
✅ Global exception handlers ✅ Custom error codes ✅ Detailed error responses

Phase 8: Testing
✅ Unit tests with pytest ✅ Integration tests ✅ 80%+ code coverage

Phase 9: CI/CD Pipeline
✅ GitHub Actions workflows ✅ Automated testing ✅ Linting and type checking ✅ Docker image building

Phase 10: Dockerization
✅ Multi-stage Docker builds ✅ Docker Compose for local development ✅ Production-optimized images

Phase 11: Kubernetes
✅ Deployment manifests ✅ Service definitions ✅ Ingress configuration ✅ StatefulSets for databases

Phase 12: AWS Deployment
✅ S3 for frontend hosting ✅ CloudFront CDN ✅ ECS Fargate for backend ✅ RDS for PostgreSQL ✅ AWS Secrets Manager ✅ CloudWatch monitoring

Phase 13: Security Hardening
✅ HTTPS/TLS enforcement ✅ Input validation with Pydantic ✅ Rate limiting ✅ Security headers ✅ CORS configuration ✅ SQL injection prevention

Phase 14: Monitoring
✅ Prometheus metrics ✅ Grafana dashboards ✅ Real-time alerts ✅ Performance tracking

Phase 15: Advanced Features
✅ AI Interview Copilot ✅ Explainable Hiring Dashboard ✅ Bias Audit Reports ✅ Market Salary Intelligence ✅ Recruiter Analytics

Phase 16: Documentation
✅ README ✅ Architecture documentation ✅ API documentation ✅ Deployment guide ✅ Security guidelines

