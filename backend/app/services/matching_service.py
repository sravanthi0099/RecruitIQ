"""Candidate-job matching service."""

from typing import List, Dict, Any, Tuple
from loguru import logger


class MatchingService:
    """Service for candidate-job matching."""

    @staticmethod
    def calculate_skill_match_score(
        candidate_skills: List[str],
        required_skills: List[str],
    ) -> float:
        """
        Calculate skill match score.
        
        Args:
            candidate_skills: List of candidate's skills
            required_skills: List of required skills
            
        Returns:
            Match score (0-1)
        """
        if not required_skills:
            return 1.0

        candidate_skills_lower = [s.lower() for s in candidate_skills]
        required_skills_lower = [s.lower() for s in required_skills]

        matches = sum(
            1 for skill in required_skills_lower
            if skill in candidate_skills_lower
        )

        return matches / len(required_skills)

    @staticmethod
    def calculate_experience_match_score(
        candidate_years: float,
        min_years: float = 0,
        max_years: float = 20,
    ) -> float:
        """
        Calculate experience match score.
        
        Args:
            candidate_years: Candidate's years of experience
            min_years: Minimum required years
            max_years: Maximum preferred years
            
        Returns:
            Match score (0-1)
        """
        if candidate_years < min_years:
            return candidate_years / min_years if min_years > 0 else 0.5

        if candidate_years > max_years:
            return 0.8 + (0.2 * (1 - (candidate_years - max_years) / max_years))

        return 1.0

    @staticmethod
    def calculate_overall_match_score(
        skill_score: float,
        experience_score: float,
        weights: Dict[str, float] = None,
    ) -> float:
        """
        Calculate overall match score.
        
        Args:
            skill_score: Skill match score
            experience_score: Experience match score
            weights: Scoring weights
            
        Returns:
            Overall match score (0-1)
        """
        if weights is None:
            weights = {
    "skills": 0.8,
    "experience": 0.2
}

        overall = (
            skill_score * weights["skills"] +
            experience_score * weights["experience"]
        )

        return min(1.0, max(0.0, overall))

    @staticmethod
    def rank_matches(
        matches: List[Dict[str, Any]],
        reverse: bool = True,
    ) -> List[Dict[str, Any]]:
        """
        Rank matches by score.
        
        Args:
            matches: List of match results
            reverse: Sort descending if True
            
        Returns:
            Sorted matches
        """
        return sorted(
            matches,
            key=lambda x: x.get("match_score", 0),
            reverse=reverse,
        )


matching_service = MatchingService()