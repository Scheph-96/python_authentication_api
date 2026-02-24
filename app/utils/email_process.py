from app.core.config import settings, Settings
from app.core.logging.logger import get_logger
from email.message import EmailMessage
from app.models.user_model import User
from app.schemas.email_validation_code import EmailValidationCode
from app.repositories.base_repository import BaseRepository
from app.utils.jwt import hash_token
from app.utils.resources import code_generator
import aiosmtplib


logger = get_logger("email_processing")


"""
    Process to send validation email with the validation code
    
    email sending runs here
    HTTP request → response returned → background task starts → email_processing()
    That is no longer inside FastAPI's request exception system
    
    so this try...except is not duplication. It's boundary protection. Since we have error_handling process and middleware
    
    Rule in distributed/backend systems:
    Every boundary(thread, background task, queue worker, scheduler) must be exception-contained because once execution leaves the request lifecycle, FastAPI is no longer responsible
"""


async def email_processing(user: User, base_repo: BaseRepository):
    try:
        # Generate validation code
        code = code_generator()
        # Create email validation record schema
        email_validation_code = EmailValidationCode(
            user_id=str(user._id), code_hash=hash_token(code)
        )

        # Insert email validation record
        email_validation_code_id = await base_repo.create(email_validation_code.model_dump())

        # Send email with the validation code
        await send_email(
            user.email,
            "Email Validation",
            verification_email_template_plain_text(code),
            verification_email_template_html(code),
        )

        logger.info(
            f"{Settings.OPERATION_SUCCESS_EVENT_LABEL}: email_sent",
            user_id=str(user._id),
            email_validation_code_id=email_validation_code_id,
        )
    except Exception as e:
        logger.error("email_send_failed", error=str(e), exc_info=True)


"""
    Email sending logic
"""


async def send_email(
    to_email: str, subject: str, plain_text_content: str, html_content: str
):
    message = EmailMessage()
    message["From"] = settings.SMTP_FROM
    message["To"] = to_email
    message["Subject"] = subject

    message.set_content(plain_text_content)
    message.add_alternative(html_content, subtype="html")

    await aiosmtplib.send(
        message,
        hostname=settings.SMTP_HOST,
        port=settings.SMTP_PORT,
        username=settings.SMTP_USER,
        password=settings.SMTP_PASSWORD,
        start_tls=True,  # TLS encryption
    )


"""
    Email Content Plain Text
"""


def verification_email_template_plain_text(code: str) -> str:
    return f"""
                {settings.COMPANY_NAME}\n
                Your validation code: {code}
            """.strip()


"""
    Email Content HTML
"""


def verification_email_template_html(code: str) -> str:
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
            """.strip()
