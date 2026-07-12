"""Analytics and reporting service."""

from typing import Dict, List, Any
from datetime import datetime, timedelta
from loguru import logger
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.candidate import Candidate


class AnalyticsService:
    """Service for analytics and reporting."""

    @staticmethod
    def calculate_funnel_metrics(db: Session) -> Dict[str, Any]:
        """
        Calculate hiring funnel metrics.
        
        Args:
            db: Database session
            
        Returns:
            Funnel metrics
        """
        statuses = {
            "new": 0,
            "screening": 0,
            "interview": 0,
            "offer": 0,
            "rejected": 0,
            "accepted": 0,
        }

        for status in statuses:
            count = db.query(func.count(Candidate.id)).filter(
                Candidate.status == status
            ).scalar()
            statuses[status] = count or 0

        total = sum(statuses.values())

        return {
            "statuses": statuses,
            "total": total,
            "conversion_rates": AnalyticsService._calculate_conversion_rates(statuses),
        }

    @staticmethod
    def _calculate_conversion_rates(statuses: Dict[str, int]) -> Dict[str, float]:
        """
        Calculate conversion rates between funnel stages.
        
        Args:
            statuses: Status counts
            
        Returns:
            Conversion rates
        """
        rates = {}

        if statuses["new"] > 0:
            rates["new_to_screening"] = statuses["screening"] / statuses["new"]

        if statuses["screening"] > 0:
            rates["screening_to_interview"] = statuses["interview"] / statuses["screening"]

        if statuses["interview"] > 0:
            rates["interview_to_offer"] = statuses["offer"] / statuses["interview"]

        if statuses["offer"] > 0:
            rates["offer_acceptance"] = statuses["accepted"] / statuses["offer"]

        return rates

    @staticmethod
    def calculate_time_to_hire(db: Session) -> float:
        """
        Calculate average time to hire.
        
        Args:
            db: Database session
            
        Returns:
            Average days to hire
        """
        # Get candidates with status "accepted"
        hired_candidates = db.query(Candidate).filter(
            Candidate.status == "accepted"
        ).all()

        if not hired_candidates:
            return 0.0

        total_days = 0
        for candidate in hired_candidates:
            if candidate.created_at:
                days = (datetime.utcnow() - candidate.created_at).days
                total_days += days

        return total_days / len(hired_candidates)

    @staticmethod
    def calculate_offer_acceptance_rate(db: Session) -> float:
        """
        Calculate offer acceptance rate.
        
        Args:
            db: Database session
            
        Returns:
            Acceptance rate (0-1)
        """
        total_offers = db.query(func.count(Candidate.id)).filter(
            Candidate.status.in_(["offer", "accepted"])
        ).scalar() or 0

        accepted = db.query(func.count(Candidate.id)).filter(
            Candidate.status == "accepted"
        ).scalar() or 0

        if total_offers == 0:
            return 0.0

        return accepted / total_offers


analytics_service = AnalyticsService()