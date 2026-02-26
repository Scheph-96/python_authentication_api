from email.message import EmailMessage
from app.core.config import Settings
from app.core.logging.logger import get_logger
import aiosmtplib

class EmailService:
    def __init__(self):
        self.logger = get_logger("email_processing")

    async def send(self, to, subject, text, html):
        try:
            message = EmailMessage()
            message["From"] = Settings.SMTP_FROM
            message["To"] = to,
            message["Subject"] = subject

            message.set_content(text) # For plain text messages
            message.add_alternative(html, subtype="html") # For html messages

            await aiosmtplib.send(
                message,
                hostname=Settings.SMTP_HOST,
                port=Settings.SMTP_PORT,
                username=Settings.SMTP_USER,
                password=Settings.SMTP_PASSWORD,
                start_tls=True,
            )
        except Exception as e:
            self.logger.error(
                "SendingEmailFailed",
                error=str(e),
                exc_info=True
            )

    def verification_email_template_plain_text(self, code: str) -> str:
        """
            Email Content Plain Text
        """
        return f"""
                    {Settings.COMPANY_NAME}\n
                    Your validation code: {code}
                """.strip()

    def verification_email_template_html(self, code: str) -> str:
        """
            Email Content HTML
        """
        return f"""
                    <html>
                        <body>
                            <h1>{Settings.COMPANY_NAME}</h1>
                            <h2>Confirm Your Email</h2>
                            <p>Here is your verification code:</p>
                            <p style="color: #1e90ff; text-align: center; font-size: 2rem">{code}</p>
                            <p>This code expire in 1 hours</p>
                            <span style="display: block; width: 100%; height: 1px; background-color: #ccc; margin-bottom: 10px"></span>
                            <small>If you did not execute this operation. Please ignore and delete this email</small>
                        </body>
                    </html>
                """.strip()
