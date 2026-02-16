from dotenv import load_dotenv
import os

load_dotenv()

class Settings:
    MONGO_URI: str = os.getenv("MONGO_URI")
    MONGO_DB_NAME: str = os.getenv("MONGO_DB_NAME")
    ENV: str = os.getenv("ENV")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
    REFRESH_TOKEN_EXPIRE_DAYS: int = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS"))
    COMPANY_NAME: str = os.getenv("COMPANY_NAME")
    ISSUER: str = os.getenv("ISSUER")
    SMTP_HOST: str = os.getenv("SMTP_HOST")
    SMTP_PORT: str = os.getenv("SMTP_PORT")
    SMTP_USER: str = os.getenv("SMTP_USER")
    SMTP_PASSWORD: str = os.getenv("SMTP_PASSWORD")
    SMTP_FROM: str = os.getenv("SMTP_FROM")
    SECURITY_EVENT_LABEL = "AuthSecurityEvent"
    OPERATION_SUCCESS_EVENT_LABEL = "OperationSuccess"
settings = Settings()