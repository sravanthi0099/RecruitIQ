from typing import Dict, Any

from app.agents.base_agent import BaseAgent


class AICandidateRanker(BaseAgent):
    """Candidate Ranking Agent."""

    def __init__(self):
        super().__init__(
            name="AICandidateRanker",
            version="1.0.0"
        )

    async def execute(
        self,
        input_data: Dict[str, Any]
    ) -> Dict[str, Any]:

        candidate_profile = input_data.get(
            "candidate_profile",
            {}
        )

        skill_gap_profile = input_data.get(
            "skill_gap_profile",
            {}
        )

        match_score = skill_gap_profile.get(
            "match_score",
            0
        )

        candidate_level = candidate_profile.get(
            "candidate_level",
            "Junior"
        )

        # Technical Fit
        technical_fit = min(
            max(match_score, 0),
            100
        )

        # Growth Potential
        level = str(candidate_level).lower()

        if "junior" in level:
            growth_potential = 90
            leadership_potential = 60
        elif "mid" in level:
            growth_potential = 80
            leadership_potential = 75
        elif "senior" in level:
            growth_potential = 70
            leadership_potential = 90
        else:
            growth_potential = 75
            leadership_potential = 70

        # Communication Score
        communication_potential = 75

        # Overall Score
        overall_score = round(
            (
                technical_fit * 0.50
                + growth_potential * 0.20
                + communication_potential * 0.15
                + leadership_potential * 0.15
            ),
            2
        )

        # Recommendation
        if overall_score >= 80:
            recommendation = "Strong Hire"
        elif overall_score >= 65:
            recommendation = "Hire"
        elif overall_score >= 50:
            recommendation = "Consider"
        else:
            recommendation = "Reject"

        reasoning = (
            f"Candidate achieved a {match_score}% skill match. "
            f"Level identified as {candidate_level}. "
            f"Technical fit={technical_fit}, "
            f"Growth potential={growth_potential}, "
            f"Leadership potential={leadership_potential}. "
            f"Final score={overall_score}."
        )

        return {
            "technical_fit": technical_fit,
            "growth_potential": growth_potential,
            "communication_potential": communication_potential,
            "leadership_potential": leadership_potential,
            "overall_score": overall_score,
            "recommendation": recommendation,
            "reasoning": reasoning
        }