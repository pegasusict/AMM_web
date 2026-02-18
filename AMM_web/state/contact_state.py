from AMM_web.state.base_state import BaseState
from AMM_web.config import settings
import smtplib
from email.message import EmailMessage


class ContactState(BaseState):
    """The state for the contact page."""

    name: str = ""
    email: str = ""
    message: str = ""
    submitted: bool = False
    submit_error: str = ""

    async def submit(self):
        """Submit the contact form and send it by email."""
        self.submitted = False
        self.submit_error = ""

        name = self.name.strip()
        email = self.email.strip()
        message = self.message.strip()

        if not name or not email or not message:
            self.submit_error = "Please fill in your name, email, and message."
            return

        msg = EmailMessage()
        msg["Subject"] = f"AMM Web contact form from {name}"
        msg["From"] = (
            settings.SMTP_FROM_EMAIL or settings.SMTP_USERNAME or settings.CONTACT_TO_EMAIL
        )
        msg["To"] = settings.CONTACT_TO_EMAIL
        msg["Reply-To"] = email
        msg.set_content(
            f"Name: {name}\n"
            f"Email: {email}\n\n"
            "Message:\n"
            f"{message}"
        )

        try:
            if settings.SMTP_USE_SSL:
                with smtplib.SMTP_SSL(
                    host=settings.SMTP_HOST,
                    port=settings.SMTP_PORT,
                    timeout=15,
                ) as smtp:
                    smtp.login(settings.SMTP_USERNAME, settings.SMTP_PASSWORD)
                    smtp.send_message(msg)
            else:
                with smtplib.SMTP(
                    host=settings.SMTP_HOST,
                    port=settings.SMTP_PORT,
                    timeout=15,
                ) as smtp:
                    if settings.SMTP_USE_TLS:
                        smtp.starttls()
                    smtp.login(settings.SMTP_USERNAME, settings.SMTP_PASSWORD)
                    smtp.send_message(msg)
        except Exception:
            self.submit_error = "Unable to send your message right now. Please try again later."
            return

        self.submitted = True
        self.name = ""
        self.email = ""
        self.message = ""
