"""Agent orchestrator for coordinating multiple agents."""

from typing import Dict, Any, List, Optional
from loguru import logger
import asyncio
from app.agents.ai_resume_agent import AIResumeAgent
from app.agents.jd_agent import JDAgent
from app.agents.skill_gap_agent import SkillGapAgent
from app.agents.ai_candidate_ranker import AICandidateRanker
from app.agents.gemini_interview_agent import GeminiInterviewAgent
from app.agents.resume_agent import ResumeAgent
from app.agents.matching_agent import MatchingAgent
from app.agents.bias_agent import BiasAgent
from app.agents.salary_agent import SalaryAgent
from app.agents.email_agent import EmailAgent
from app.agents.interview_agent import InterviewAgent


class AgentOrchestrator:
    """Orchestrates execution of multiple AI agents."""

    def __init__(self):
        """Initialize Agent Orchestrator."""
        self.ai_resume_agent = AIResumeAgent()
        self.jd_agent = JDAgent()
        self.skill_gap_agent = SkillGapAgent()
        self.candidate_ranker = AICandidateRanker()
        self.gemini_interview_agent = GeminiInterviewAgent()
        self.resume_agent = ResumeAgent()
        self.matching_agent = MatchingAgent()
        self.bias_agent = BiasAgent()
        self.salary_agent = SalaryAgent()
        self.email_agent = EmailAgent()
        self.interview_agent = InterviewAgent()

        logger.info("AgentOrchestrator initialized with all agents")
    
    

    async def analyze_resume(self, resume_text: str) -> Dict[str, Any]:
        """
        Analyze resume using Resume Agent.
        
        Args:
            resume_text: Resume text
            
        Returns:
            Analysis result
        """
        logger.info("AgentOrchestrator: Starting resume analysis")

        result = await self.resume_agent._execute_with_logging({
            "resume_text": resume_text,
        })

        return result

    async def match_candidate_to_job(
        self,
        candidate_skills: List[str],
        required_skills: List[str],
        candidate_years: float,
        min_years: float = 0,
        max_years: float = 20,
    ) -> Dict[str, Any]:
        """
        Match candidate to job using Matching Agent.
        
        Args:
            candidate_skills: Candidate's skills
            required_skills: Required skills
            candidate_years: Candidate's experience
            min_years: Minimum required experience
            max_years: Maximum preferred experience
            
        Returns:
            Matching result
        """
        logger.info("AgentOrchestrator: Starting candidate-job matching")

        result = await self.matching_agent._execute_with_logging({
            "candidate_skills": candidate_skills,
            "required_skills": required_skills,
            "candidate_years": candidate_years,
            "min_years": min_years,
            "max_years": max_years,
        })

        return result
    

    async def audit_bias(
        self,
        candidates: List[Dict[str, Any]],
        job_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Audit bias in candidate pool using Bias Agent.
        
        Args:
            candidates: List of candidates
            job_id: Optional job ID
            
        Returns:
            Bias audit result
        """
        logger.info("AgentOrchestrator: Starting bias audit")

        result = await self.bias_agent._execute_with_logging({
            "candidates": candidates,
            "job_id": job_id,
        })

        return result

    async def estimate_salary(
        self,
        job_title: str,
        location: str,
        experience_years: float = 0,
        skills: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """
        Estimate salary using Salary Agent.
        
        Args:
            job_title: Job title
            location: Job location
            experience_years: Years of experience
            skills: List of skills
            
        Returns:
            Salary estimation result
        """
        logger.info("AgentOrchestrator: Starting salary estimation")

        result = await self.salary_agent._execute_with_logging({
            "job_title": job_title,
            "location": location,
            "experience_years": experience_years,
            "skills": skills or [],
        })

        return result

    async def generate_email(
        self,
        candidate_name: str,
        job_title: str,
        email_type: str,
        company_name: str = "Our Company",
    ) -> Dict[str, Any]:
        """
        Generate recruitment email using Email Agent.
        
        Args:
            candidate_name: Candidate name
            job_title: Job title
            email_type: Type of email
            company_name: Company name
            
        Returns:
            Generated email
        """
        logger.info("AgentOrchestrator: Starting email generation")

        result = await self.email_agent._execute_with_logging({
            "candidate_name": candidate_name,
            "job_title": job_title,
            "email_type": email_type,
            "company_name": company_name,
        })

        return result

    async def generate_interview_questions(
        self,
        skills: List[str],
        difficulty: str = "medium",
        num_questions: int = 5,
    ) -> Dict[str, Any]:
        """
        Generate interview questions using Interview Agent.
        
        Args:
            skills: Candidate's skills
            difficulty: Difficulty level
            num_questions: Number of questions
            
        Returns:
            Generated interview questions
        """
        logger.info("AgentOrchestrator: Starting interview question generation")

        result = await self.interview_agent._execute_with_logging({
            "skills": skills,
            "difficulty": difficulty,
            "num_questions": num_questions,
        })

        return result

    async def run_full_analysis(
        self,
        resume_text: str,
        required_skills: List[str],
        job_title: str,
        location: str,
    ) -> Dict[str, Any]:
        """
        Run full candidate analysis using multiple agents.
        
        Args:
            resume_text: Resume text
            required_skills: Required skills
            job_title: Job title
            location: Job location
            
        Returns:
            Comprehensive analysis result
        """
        logger.info("AgentOrchestrator: Starting full candidate analysis")

        # Run agents concurrently
        resume_result = await self.analyze_resume(resume_text)
        
        if resume_result["status"] == "completed":
            resume_data = resume_result.get("result", {})
            
            # Run matching
            matching_result = await self.match_candidate_to_job(
                candidate_skills=resume_data.get("skills", []),
                required_skills=required_skills,
                candidate_years=resume_data.get("experience_years", 0),
            )

            # Run salary estimation
            salary_result = await self.estimate_salary(
                job_title=job_title,
                location=location,
                experience_years=resume_data.get("experience_years", 0),
                skills=resume_data.get("skills", []),
            )

            # Run interview question generation
            interview_result = await self.generate_interview_questions(
                skills=resume_data.get("skills", []),
                difficulty="medium",
                num_questions=5,
            )

            return {
                "status": "completed",
                "resume_analysis": resume_result,
                "matching_analysis": matching_result,
                "salary_estimation": salary_result,
                "interview_questions": interview_result,
            }
        else:
            return {
                "status": "failed",
                "error": "Resume analysis failed",
            }