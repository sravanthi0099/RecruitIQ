"""Bias detection and analysis agent."""

from typing import Dict, Any, List
from loguru import logger

from app.agents.base_agent import BaseAgent


class BiasAgent(BaseAgent):
    """Agent for detecting and analyzing bias in hiring."""

    def __init__(self):
        """Initialize Bias Agent."""
        super().__init__(name="BiasAgent", version="1.0.0")

    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute bias analysis.
        
        Args:
            input_data: Candidate pool and job data
            
        Returns:
            Bias analysis result
        """
        candidates = input_data.get("candidates", [])
        job_id = input_data.get("job_id")

        logger.info(
            f"{self.name}: Analyzing bias",
            extra={"job_id": job_id, "candidate_count": len(candidates)},
        )

        if not candidates:
            return {
                "bias_score": 0.0,
                "gender_diversity": {},
                "education_diversity": {},
                "geographic_diversity": {},
                "recommendations": [],
            }

        # Analyze diversity metrics
        gender_diversity = self._analyze_gender_diversity(candidates)
        education_diversity = self._analyze_education_diversity(candidates)
        geographic_diversity = self._analyze_geographic_diversity(candidates)

        # Calculate overall bias score
        bias_score = self._calculate_bias_score(
            gender_diversity,
            education_diversity,
            geographic_diversity,
        )

        # Generate recommendations
        recommendations = self._generate_recommendations(
            bias_score,
            gender_diversity,
            education_diversity,
            geographic_diversity,
        )

        result = {
            "bias_score": round(bias_score, 3),
            "gender_diversity": gender_diversity,
            "education_diversity": education_diversity,
            "geographic_diversity": geographic_diversity,
            "recommendations": recommendations,
            "total_candidates_analyzed": len(candidates),
        }

        logger.info(
            f"{self.name}: Analysis complete",
            extra={"bias_score": bias_score},
        )

        return result

    def _analyze_gender_diversity(self, candidates: List[Dict[str, Any]]) -> Dict[str, float]:
        """
        Analyze gender diversity.
        
        Args:
            candidates: List of candidates
            
        Returns:
            Gender diversity metrics
        """
        if not candidates:
            return {}

        total = len(candidates)
        
        # This is placeholder - would use ML model for gender inference
        male_count = sum(1 for c in candidates if c.get("gender") == "male")
        female_count = sum(1 for c in candidates if c.get("gender") == "female")
        other_count = total - male_count - female_count

        return {
            "male_percentage": round((male_count / total) * 100, 2),
            "female_percentage": round((female_count / total) * 100, 2),
            "other_percentage": round((other_count / total) * 100, 2),
            "is_balanced": 40 <= (female_count / total) * 100 <= 60,
        }

    def _analyze_education_diversity(self, candidates: List[Dict[str, Any]]) -> Dict[str, float]:
        """
        Analyze educational background diversity.
        
        Args:
            candidates: List of candidates
            
        Returns:
            Education diversity metrics
        """
        if not candidates:
            return {}

        total = len(candidates)
        top_school_count = 0
        state_school_count = 0
        other_count = 0

        # Placeholder logic
        for candidate in candidates:
            school = candidate.get("education_school", "").lower()
            if any(ts in school for ts in ["mit", "stanford", "harvard", "berkeley"]):
                top_school_count += 1
            elif any(ss in school for ss in ["state", "university"]):
                state_school_count += 1
            else:
                other_count += 1

        return {
            "top_schools_percentage": round((top_school_count / total) * 100, 2),
            "state_schools_percentage": round((state_school_count / total) * 100, 2),
            "other_percentage": round((other_count / total) * 100, 2),
            "is_diverse": top_school_count / total < 0.5,
        }

    def _analyze_geographic_diversity(self, candidates: List[Dict[str, Any]]) -> Dict[str, float]:
        """
        Analyze geographic diversity.
        
        Args:
            candidates: List of candidates
            
        Returns:
            Geographic diversity metrics
        """
        if not candidates:
            return {}

        total = len(candidates)
        locations = [c.get("location", "").lower() for c in candidates]

        # Placeholder: categorize by region
        urban_count = sum(1 for loc in locations if any(u in loc for u in ["ny", "la", "sf", "chicago"]))
        suburban_count = total - urban_count
        rural_count = 0

        return {
            "urban_percentage": round((urban_count / total) * 100, 2),
            "suburban_percentage": round((suburban_count / total) * 100, 2),
            "rural_percentage": round((rural_count / total) * 100, 2),
            "is_diverse": urban_count / total < 0.7,
        }

    def _calculate_bias_score(
        self,
        gender_diversity: Dict[str, Any],
        education_diversity: Dict[str, Any],
        geographic_diversity: Dict[str, Any],
    ) -> float:
        """
        Calculate overall bias score.
        
        Args:
            gender_diversity: Gender metrics
            education_diversity: Education metrics
            geographic_diversity: Geographic metrics
            
        Returns:
            Bias score (0-1, where 1 is least biased)
        """
        score = 0.0
        metrics = 0

        # Gender balance score
        if gender_diversity.get("is_balanced"):
            score += 0.33
        metrics += 1

        # Education diversity score
        if education_diversity.get("is_diverse"):
            score += 0.33
        metrics += 1

        # Geographic diversity score
        if geographic_diversity.get("is_diverse"):
            score += 0.34
        metrics += 1

        return score / metrics if metrics > 0 else 0.5

    def _generate_recommendations(
        self,
        bias_score: float,
        gender_diversity: Dict[str, Any],
        education_diversity: Dict[str, Any],
        geographic_diversity: Dict[str, Any],
    ) -> List[str]:
        """
        Generate recommendations to reduce bias.
        
        Args:
            bias_score: Overall bias score
            gender_diversity: Gender metrics
            education_diversity: Education metrics
            geographic_diversity: Geographic metrics
            
        Returns:
            List of recommendations
        """
        recommendations = []

        if bias_score < 0.6:
            recommendations.append("This candidate pool shows significant diversity gaps. Consider expanding recruitment channels.")

        if not gender_diversity.get("is_balanced"):
            recommendations.append("Work towards better gender balance in candidate pool.")

        if not education_diversity.get("is_diverse"):
            recommendations.append("Expand recruitment to include candidates from diverse educational backgrounds.")

        if not geographic_diversity.get("is_diverse"):
            recommendations.append("Increase geographic diversity in recruitment efforts.")

        if not recommendations:
            recommendations.append("Candidate pool shows good diversity metrics. Maintain current practices.")

        return recommendations