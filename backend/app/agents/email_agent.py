"""Email communication agent."""

from typing import Dict, Any
from loguru import logger

from app.agents.base_agent import BaseAgent


class EmailAgent(BaseAgent):
    """Agent for generating recruitment emails."""

    def __init__(self):
        """Initialize Email Agent."""
        super().__init__(name="EmailAgent", version="1.0.0")

    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute email generation.
        
        Args:
            input_data: Candidate info, job info, email type
            
        Returns:
            Generated email
        """
        candidate_name = input_data.get("candidate_name", "Candidate")
        job_title = input_data.get("job_title", "Position")
        email_type = input_data.get("email_type", "initial_outreach")  # initial_outreach, interview_invitation, offer, rejection
        company_name = input_data.get("company_name", "Our Company")

        logger.info(
            f"{self.name}: Generating email",
            extra={
                "candidate": candidate_name,
                "email_type": email_type,
            },
        )

        email_templates = {
            "initial_outreach": self._generate_outreach_email(candidate_name, job_title, company_name),
            "interview_invitation": self._generate_interview_email(candidate_name, job_title, company_name),
            "offer": self._generate_offer_email(candidate_name, job_title, company_name),
            "rejection": self._generate_rejection_email(candidate_name, company_name),
        }

        email_content = email_templates.get(email_type, email_templates["initial_outreach"])

        result = {
            "email_type": email_type,
            "subject": email_content["subject"],
            "body": email_content["body"],
            "recipient": candidate_name,
        }

        logger.info(f"{self.name}: Email generated successfully")

        return result

    def _generate_outreach_email(self, candidate_name: str, job_title: str, company_name: str) -> Dict[str, str]:
        """Generate initial outreach email."""
        return {
            "subject": f"Great opportunity: {job_title} at {company_name}",
            "body": f"""Dear {candidate_name},

We came across your profile and think you'd be a great fit for our {job_title} position at {company_name}.

We're looking for talented professionals like you to join our growing team. If you're interested in learning more about this opportunity, we'd love to chat.

Best regards,
The {company_name} Team""",
        }

    def _generate_interview_email(self, candidate_name: str, job_title: str, company_name: str) -> Dict[str, str]:
        """Generate interview invitation email."""
        return {
            "subject": f"Interview Invitation: {job_title} at {company_name}",
            "body": f"""Dear {candidate_name},

We're pleased to invite you to interview for the {job_title} position at {company_name}.

The interview will take approximately 60 minutes and will cover your background, experience, and interest in the role.

Please let us know your availability for the next week.

Best regards,
The {company_name} Team""",
        }

    def _generate_offer_email(self, candidate_name: str, job_title: str, company_name: str) -> Dict[str, str]:
        """Generate job offer email."""
        return {
            "subject": f"Job Offer: {job_title} at {company_name}",
            "body": f"""Dear {candidate_name},

Congratulations! We're excited to extend a formal offer for the {job_title} position at {company_name}.

The details of the offer are included in the attached document. Please review and let us know if you have any questions.

We look forward to welcoming you to our team!

Best regards,
The {company_name} Team""",
        }

    def _generate_rejection_email(self, candidate_name: str, company_name: str) -> Dict[str, str]:
        """Generate rejection email."""
        return {
            "subject": f"Application Status Update",
            "body": f"""Dear {candidate_name},

Thank you for your interest in {company_name} and the time you invested in our interview process.

While you have impressive qualifications, we've decided to move forward with other candidates whose experience more closely aligns with our current needs.

We encourage you to apply for future opportunities that match your skillset.

Best regards,
The {company_name} Team""",
        }