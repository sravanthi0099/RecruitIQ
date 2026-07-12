class EmailTemplates:

    @staticmethod
    def shortlist_email(
        candidate_name: str,
        job_title: str
    ):

        subject = (
            f"Shortlisted for {job_title}"
        )

        body = f"""
Dear {candidate_name},

Congratulations!

Based on our AI-powered screening process,
you have been shortlisted for the role:

{job_title}

Our recruitment team will contact you shortly
with the next steps.

Best Regards,
RecruitIQ Hiring Team
"""

        return subject, body

    @staticmethod
    def rejection_email(
        candidate_name: str,
        job_title: str
    ):

        subject = (
            f"Application Update - {job_title}"
        )

        body = f"""
Dear {candidate_name},

Thank you for applying for
{job_title}.

After careful review,
we have decided not to move forward
with your application.

We wish you success in your future career.

Best Regards,
RecruitIQ Hiring Team
"""

        return subject, body

    @staticmethod
    def interview_invite_email(
        candidate_name: str,
        job_title: str,
        interview_date: str,
        interview_link: str
    ):

        subject = (
            f"Interview Invitation - {job_title}"
        )

        body = f"""
Dear {candidate_name},

Congratulations!

You have been selected for the next stage
of our hiring process.

Interview Details

Position:
{job_title}

Date:
{interview_date}

Meeting Link:
{interview_link}

Please join the interview on time.

Best Regards,
RecruitIQ Hiring Team
"""

        return subject, body