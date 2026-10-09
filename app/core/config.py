import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import MetaData

load_dotenv()


class Settings:
    #################### CONFIG SETTINGS ####################
    # -------------- ENVIRONMENT VARIABLES -------------- #
    # ------- Required -------
    APP_HOST: str = os.environ["APP_HOST"]
    APP_PORT: int = int(os.environ["APP_PORT"])
    ENV: str = os.environ["ENV"]
    DATABASE_URI: str = os.environ["DATABASE_URI"]
    DATABASE_NAME: str = os.environ["DATABASE_NAME"]
    PRIVATE_KEY_PATH: str = os.path.join(Path(__file__).resolve().parent.parent, os.environ["PRIVATE_KEY_PATH"])
    PUBLIC_KEY_PATH: str = os.path.join(Path(__file__).resolve().parent.parent, os.environ["PUBLIC_KEY_PATH"])
    ACCESS_TOKEN_EXPIRATION_MINUTES: int = int(os.environ["ACCESS_TOKEN_EXPIRATION_MINUTES"])
    REFRESH_TOKEN_EXPIRATION_DAYS: int = int(os.environ["REFRESH_TOKEN_EXPIRATION_DAYS"])
    PASSWORD_RECOVERY_TOKEN_EXPIRATION_MINUTES: int = int(os.environ["PASSWORD_RECOVERY_TOKEN_EXPIRATION_MINUTES"])
    EMAIL_VALIDATION_CODE_EXPIRATION_HOURS: int = int(os.environ["EMAIL_VALIDATION_CODE_EXPIRATION_HOURS"])
    # ------- Optional -------
    API_PREFIX: str = os.getenv("API_PREFIX", "rbac_api")
    COMPANY_NAME: str = os.getenv("COMPANY_NAME", "MY_COMPANY INC.")
    ISSUER: str = os.getenv("ISSUER", "APP_RBAC_API")
    SMTP_HOST: str = os.getenv("SMTP_HOST", "")
    SMTP_PORT: int = int(os.getenv("SMTP_PORT", "0"))
    SMTP_USER: str = os.getenv("SMTP_USER", "")
    SMTP_PASSWORD: str = os.getenv("SMTP_PASSWORD", "")
    SMTP_FROM: str = os.getenv("SMTP_FROM", "")
    SECURITY_EVENT_LABEL = "AuthSecurityEvent"
    OPERATION_SUCCESS_EVENT_LABEL = "OperationSuccess"
    # -------------- APP PARAMETERS -------------- #
    SQLALCHEMY_METADATA: MetaData = MetaData()
    ACTIVATE_AUTHORIZATION_INTERFACE = True

    #################### COLLECTIONS NAME ####################

    # -------------- AUTHENTICATION -------------- #
    USERS_COLLECTION: str = "users"
    EMAIL_VALIDATION_CODE_COLLECTION: str = "email_validation_codes"
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
    ROLE_ASSIGNMENT: bool = False

# settings = Settings()
