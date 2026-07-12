from email.message import EmailMessage
import aiosmtplib

from app.config import settings


class EmailService:

    async def send_email(
        self,
        to_email: str,
        subject: str,
        body: str
    ):

        message = EmailMessage()

        message["From"] = settings.SMTP_EMAIL
        message["To"] = to_email
        message["Subject"] = subject

        message.set_content(body)

        await aiosmtplib.send(
            message,
            hostname=settings.SMTP_HOST,
            port=settings.SMTP_PORT,
            start_tls=True,
            username=settings.SMTP_EMAIL,
            password=settings.SMTP_PASSWORD,
        )


email_service = EmailService()