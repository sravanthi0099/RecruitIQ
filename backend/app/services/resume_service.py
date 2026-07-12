"""Resume processing service."""

import re
from typing import Dict, List, Any
from loguru import logger


class ResumeService:
    """Service for resume processing and extraction."""

    @staticmethod
    def extract_skills(text: str) -> List[str]:
        """
        Extract skills from resume text.
        
        Args:
            text: Resume text
            
        Returns:
            List of extracted skills
        """
        # Common technical skills to look for
        technical_skills = [
    "Python",
    "Java",
    "JavaScript",
    "TypeScript",
    "C",
    "C++",
    "C#",
    "SQL",
    "MySQL",
    "PostgreSQL",
    "MongoDB",
    "Oracle",
    "React",
    "Angular",
    "Vue",
    "Node.js",
    "Express",
    "Django",
    "Flask",
    "FastAPI",
    "Spring Boot",
    "AWS",
    "Azure",
    "GCP",
    "Docker",
    "Kubernetes",
    "Git",
    "GitHub",
    "Linux",
    "Machine Learning",
    "Deep Learning",
    "TensorFlow",
    "PyTorch",
    "Pandas",
    "NumPy",
    "Scikit-learn",
    "Power BI",
    "Tableau",
    "Data Analysis",
    "HTML",
    "CSS",
    "REST API"
]
        found_skills = []
        text_lower = text.lower()

        for skill in technical_skills:
            if skill.lower() in text_lower:
                found_skills.append(skill)

        return found_skills

    @staticmethod
    def extract_experience_years(text: str) -> float:
        """
        Extract years of experience from resume text.
        
        Args:
            text: Resume text
            
        Returns:
            Estimated years of experience
        """
        # Look for patterns like "5 years", "10+ years", etc.
        pattern = r'(\d+)\s*\+?\s*(?:years?|yrs?)'
        matches = re.findall(pattern, text, re.IGNORECASE)

        if matches:
            years = [int(m) for m in matches]
            return max(years)

        return 0.0

    @staticmethod
    def calculate_readability_score(text: str) -> float:
        """
        Calculate readability score for resume.
        
        Args:
            text: Resume text
            
        Returns:
            Readability score (0-100)
        """
        if not text:
            return 0.0

        # Simple readability metrics
        sentences = text.split('.')
        words = text.split()
        
        if not sentences or not words:
            return 0.0

        avg_sentence_length = len(words) / max(len(sentences), 1)
        
        # Scoring: optimal is 15-20 words per sentence
        if avg_sentence_length < 10:
            score = 50
        elif avg_sentence_length < 15:
            score = 75
        elif avg_sentence_length < 25:
            score = 90
        else:
            score = 70

        return min(100, score)

    @staticmethod
    def calculate_completeness_score(extracted_data: Dict[str, Any]) -> float:
        """
        Calculate completeness score based on extracted fields.
        
        Args:
            extracted_data: Extracted resume data
            
        Returns:
            Completeness score (0-100)
        """
        required_fields = ['skills', 'experience', 'education']
        score = 0

        for field in required_fields:
            if field in extracted_data and extracted_data[field]:
                score += 33

        return min(100, score)


resume_service = ResumeService()