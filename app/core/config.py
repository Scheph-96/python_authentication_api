from dotenv import load_dotenv
import os

load_dotenv()

class Settings:
    #################### CONFIG SETTINGS ####################
    MONGO_URI: str = os.getenv("MONGO_URI")
    MONGO_DB_NAME: str = os.getenv("MONGO_DB_NAME")
    ENV: str = os.getenv("ENV")
    API_PREFIX: str = os.getenv("API_PREFIX")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
    REFRESH_TOKEN_EXPIRE_DAYS: int = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS"))
    COMPANY_NAME: str = os.getenv("COMPANY_NAME")
    ISSUER: str = os.getenv("ISSUER")
    SMTP_HOST: str = os.getenv("SMTP_HOST")
    SMTP_PORT: int = int(os.getenv("SMTP_PORT"))
    SMTP_USER: str = os.getenv("SMTP_USER")
    SMTP_PASSWORD: str = os.getenv("SMTP_PASSWORD")
    SMTP_FROM: str = os.getenv("SMTP_FROM")
    SECURITY_EVENT_LABEL = "AuthSecurityEvent"
    OPERATION_SUCCESS_EVENT_LABEL = "OperationSuccess"

    #################### COLLECTIONS NAME ####################

    # -------------- AUTHENTICATION -------------- #
    USERS_COLLECTION: str = "users"
    EMAIL_VALIDATION_CODE_COLLECTION: str = "email_validation_code"
    REFRESH_TOKENS_COLLECTION: str = "refresh_tokens"
    PASSWORD_RECOVERY_TOKENS_COLLECTION: str = "password_recovery_tokens"
    # -------------- AUTHORIZATION -------------- #
    ROLES_COLLECTION: str = "roles"
    PERMISSIONS_COLLECTION: str = "permissions"
    ROLE_PERMISSIONS_COLLECTION: str = "role_permissions"
    USER_ROLES_COLLECTION: str = "user_roles"

    #################### PIPELINE SETTINGS ####################
    # Set to true to enable or false to disable

    # -------------- REGISTRATION -------------- #
    EMAIL_VALIDATION: bool = False
    ROLE_ASSIGNMENT: bool = True

settings = Settings()