"""Resume extraction and analysis agent."""

from typing import Dict, Any, List
from loguru import logger
import re

from app.agents.base_agent import BaseAgent
from app.services.resume_service import resume_service


class ResumeAgent(BaseAgent):
    """Agent for resume extraction and analysis."""

    def __init__(self):
        """Initialize Resume Agent."""
        super().__init__(name="ResumeAgent", version="1.0.0")

    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute resume analysis.
        
        Args:
            input_data: Must contain 'resume_text' key
            
        Returns:
            Resume analysis result
        """
        resume_text = input_data.get("resume_text", "")
        
        if not resume_text:
            raise ValueError("resume_text is required")

        logger.info(f"{self.name}: Analyzing resume", extra={"text_length": len(resume_text)})

        # Extract information
        skills = resume_service.extract_skills(resume_text)
        experience_years = resume_service.extract_experience_years(resume_text)
        education = self._extract_education(resume_text)
        certifications = self._extract_certifications(resume_text)
        
        # Calculate scores
        readability_score = resume_service.calculate_readability_score(resume_text)
        
        extracted_data = {
            "skills": skills,
            "experience": experience_years,
            "education": education,
            "certifications": certifications,
        }
        
        completeness_score = resume_service.calculate_completeness_score(extracted_data)

        result = {
            "skills": skills,
            "experience_years": experience_years,
            "education": education,
            "certifications": certifications,
            "readability_score": readability_score,
            "completeness_score": completeness_score,
            "summary": self._generate_summary(skills, experience_years),
            "confidence_score": self._calculate_confidence(resume_text, extracted_data),
        }

        logger.info(
            f"{self.name}: Analysis complete",
            extra={
                "skills_found": len(skills),
                "experience_years": experience_years,
                "confidence": result["confidence_score"],
            },
        )

        return result

    def _extract_education(self, text: str) -> List[Dict[str, Any]]:
        """
        Extract education information.
        
        Args:
            text: Resume text
            
        Returns:
            List of education entries
        """
        degrees = ["BS", "BA", "MS", "MA", "PhD", "MBA", "BBA"]
        education = []

        for degree in degrees:
            if degree in text:
                education.append({
                    "degree": degree,
                    "field": "Unknown",
                    "school": "Unknown",
                })

        return education

    def _extract_certifications(self, text: str) -> List[str]:
        """
        Extract certifications.
        
        Args:
            text: Resume text
            
        Returns:
            List of certifications
        """
        certifications = [
            "AWS Certified Solutions Architect",
            "Certified Kubernetes Administrator",
            "Google Cloud Professional",
            "Azure Solutions Architect",
            "PMP",
            "CISSP",
        ]

        found = []
        text_lower = text.lower()

        for cert in certifications:
            if cert.lower() in text_lower:
                found.append(cert)

        return found

    def _generate_summary(self, skills: List[str], experience_years: float) -> str:
        """
        Generate resume summary.
        
        Args:
            skills: Extracted skills
            experience_years: Years of experience
            
        Returns:
            Summary text
        """
        if not skills and experience_years == 0:
            return "Unable to generate summary from resume."

        summary_parts = []

        if experience_years > 0:
            summary_parts.append(f"Experienced professional with {experience_years:.0f} years of experience")

        if skills:
            top_skills = ", ".join(skills[:3])
            summary_parts.append(f"Skilled in {top_skills}")

        return ". ".join(summary_parts) + "." if summary_parts else "Professional profile available."

    def _calculate_confidence(self, text: str, extracted_data: Dict[str, Any]) -> float:
        """
        Calculate extraction confidence score.
        
        Args:
            text: Resume text
            extracted_data: Extracted data
            
        Returns:
            Confidence score (0-1)
        """
        score = 0.5  # Base score

        # Increase score if we found data
        if extracted_data.get("skills"):
            score += 0.15
        if extracted_data.get("education"):
            score += 0.15
        if extracted_data.get("experience") and extracted_data["experience"] > 0:
            score += 0.15

        # Decrease if text is too short
        if len(text) < 500:
            score -= 0.1

        return min(1.0, max(0.0, score))