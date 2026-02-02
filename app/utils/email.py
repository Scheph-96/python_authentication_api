from app.core.config import settings
from email.message import EmailMessage
import aiosmtplib

async def send_email(to_email: str, subject: str, html_content: str):
    message = EmailMessage()
    message["From"] = settings.SMTP_FROM
    message["To"] = to_email
    message["Subject"] = subject
    
    message.set_content("Your email client does not support HTML.")
    message.add_alternative(html_content, subtype="html")
    
    await aiosmtplib.send(
        message,
        hostname=settings.SMTP_HOST,
        port=settings.SMTP_PORT,
        username=settings.SMTP_USER,
        password=settings.SMTP_PASSWORD,
        start_tls=True, #TLS encryption
    )
    
def verification_email_template(code: str) -> str:
    return f"""
        <html>
            <body>
                <h1>{settings.COMPANY_NAME}</h1>
                <h2>Confirm Your Email</h2>
                <p>Here is your verification code:</p>
                <p style="color: #1e90ff; text-align: center; font-size: 2rem">{code}</p>
                <p>This code expire in 1 hours</p>
                <span style="display: block; width: 100%; height: 1px; background-color: #ccc; margin-bottom: 10px"></span>
                <small>If you did not execute this operation. Please ignore and delete this email</small>
            </body>
        </html>
        """