from fastapi import APIRouter, Depends, BackgroundTasks

from app.core.config import Settings
from app.database.document.db_motor import db
from app.models.dependencies_model.authentication_dependencies import AuthenticationDependencies
from app.repositories.document.authentication_repositories.email_validation_code_repository import EmailValidationCodeRepository
from app.repositories.document.authentication_repositories.password_recovery_token_repository import (
    PasswordRecoveryTokenRepository,
)
from app.repositories.document.authentication_repositories.refresh_token_repository import RefreshTokenRepository
from app.repositories.document.authentication_repositories.user_repository import UserRepository
from app.schemas.authentication_schemas.email_validation_code_schema import (
    EmailValidationCodeSubmit,
    EmailValidationCodeRetry,
)
from app.schemas.authentication_schemas.password_recovery_token_schema import (
    PasswordRecoveryConfirmEmailSchema,
    PasswordRecoveryResetPasswordSchema,
)
from app.schemas.authentication_schemas.refresh_token_schema import RefreshTokenSchema
from app.schemas.authentication_schemas.user_schema import UserSignUpSchema, UserSignInSchema, UserLogOutSchema
from app.services.core_services.authentication.authentication_service import AuthenticationService
from app.services.core_services.authentication.model_services.email_validation_code_service import EmailValidationCodeService
from app.services.core_services.authentication.model_services.password_recovery_token_service import PasswordRecoveryTokenService
from app.services.core_services.authentication.model_services.refresh_token_service import RefreshTokenService
from app.services.core_services.authentication.model_services.user_service import UserService
from app.utils.resources import api_response

# from app.utils.jwt import verify_access_token

router = APIRouter(prefix=f"{Settings.API_PREFIX}/authenticate")


########################################### DEPENDENCIES ###########################################


# Dependency: emailValidation repository
def get_email_validation_repository():
    return EmailValidationCodeRepository(db[Settings.EMAIL_VALIDATION_CODE_COLLECTION])


# Dependency: user repository
def get_user_repository():
    return UserRepository(db[Settings.USERS_COLLECTION])


# Dependency: refreshToken repository
def get_refresh_token_repository():
    return RefreshTokenRepository(db[Settings.REFRESH_TOKENS_COLLECTION])


# Dependency: passwordRecoveryToken repository
def get_password_recovery_token_repository():
    return PasswordRecoveryTokenRepository(db[Settings.PASSWORD_RECOVERY_TOKENS_COLLECTION])


# Dependency: emailValidation Service
def get_email_validation_code_service(
        repo: EmailValidationCodeRepository = Depends(get_email_validation_repository)
):
    return EmailValidationCodeService(repo)


# Dependency: user service
def get_user_service(
        repo: UserRepository = Depends(get_user_repository)
):
    return UserService(repo)


# Dependency: refreshToken service
def get_refresh_token_service(
        refresh_token_repo: RefreshTokenRepository = Depends(get_refresh_token_repository),
        user_repo: UserRepository = Depends(get_user_repository)
):
    return RefreshTokenService(refresh_token_repo, user_repo)


# Dependency: passwordRecovery service
def get_password_recovery_token_service(
        repo: PasswordRecoveryTokenRepository = Depends(
            get_password_recovery_token_repository
        ),
):
    return PasswordRecoveryTokenService(repo)


# Dependency: authentication service
def get_auth_service(
        background_tasks: BackgroundTasks,
        user_service: UserService = Depends(get_user_service),
        refresh_token_service: RefreshTokenService = Depends(get_refresh_token_service),
        password_recovery_token_service: PasswordRecoveryTokenService = Depends(
            get_password_recovery_token_service
        ),
        email_validation_code_service: EmailValidationCodeService = Depends(
            get_email_validation_code_service),
):
    return AuthenticationService(
        AuthenticationDependencies(user_service=user_service, refresh_token_service=refresh_token_service,
                                   password_recovery_token_service=password_recovery_token_service,
                                   email_validation_code_service=email_validation_code_service,
                                   background_tasks=background_tasks)
    )


########################################### ENDPOINTS ###########################################


"""
    This endpoint create users account
"""


@router.post("/register", response_model=dict)
async def user_registration(
        user: UserSignUpSchema,
        authentication_service: AuthenticationService = Depends(get_auth_service)
):
    user_id = await authentication_service.user_registration(user.model_dump())
    return api_response(
        success=True, data={"user_id": user_id}, message="User created successfully"
    )


"""
    This endpoint authenticate our users
"""


@router.post("/login", response_model=dict)
async def user_login(
        user: UserSignInSchema,
        authentication_service: AuthenticationService = Depends(get_auth_service)
):
    auth_token = await authentication_service.login(user.model_dump())

    return api_response(success=True, data=auth_token)


"""
    The endpoint that will log users out
"""


@router.post("/logout", response_model=dict)
async def logout(user: UserLogOutSchema, authentication_service: AuthenticationService = Depends(get_auth_service)):
    result = await authentication_service.logout(user.model_dump())

    return api_response(success=True, data=result)


"""
    This endpoint verify users account when they provide the validation code that was sent to their email address
"""


@router.post("/validate_email", response_model=dict)
async def validate_email(
        data: EmailValidationCodeSubmit,
        authentication_service: AuthenticationService = Depends(get_auth_service)
):
    result = await authentication_service.validate_verification_code(data.model_dump())

    return api_response(success=True, data=result)


"""
    In case the account validation email was not sent (for any reason), this endpoint ensure the retry process
"""


@router.post("/validate_email/retry", response_model=dict)
async def retry(
        data: EmailValidationCodeRetry,
        authentication_service: AuthenticationService = Depends(get_auth_service),
):
    result = await authentication_service.resend_validation_code(data.model_dump())

    return api_response(success=True, message=result)


"""
    Refresh users access token with the provided refresh token, a new access token is generated with the refresh token
"""


@router.post("/refresh/tokens")
async def refresh_token(
        refresh_token: RefreshTokenSchema,
        authentication_service: AuthenticationService = Depends(get_auth_service),
):
    new_tokens = await authentication_service.refresh_token(refresh_token.model_dump())

    return api_response(success="True", message="New Token Generated", data=new_tokens)


"""
    We check the email address provided by the user in the password recovery process
"""


@router.post("/password_recovery/forgot")
async def password_forgot(
        password_recovery_confirm_email: PasswordRecoveryConfirmEmailSchema,
        authentication_service: AuthenticationService = Depends(get_auth_service),
):
    password_recovery_token = await authentication_service.password_recovery_confirm_email(
        password_recovery_confirm_email.model_dump()
    )

    return api_response(
        success=True,
        message="If this email exists, a reset link has been sent",
        data=password_recovery_token,
    )


"""
    Now that the email address is validate and the token generated, let's reset the password
"""


@router.post("/password_recovery/reset")
async def password_reset(
        password_recovery_reset_password: PasswordRecoveryResetPasswordSchema,
        authentication_service: AuthenticationService = Depends(get_auth_service),
):
    result = await authentication_service.password_recovery_reset_password(
        password_recovery_reset_password.model_dump())

    return api_response(
        success=True,
        message=result,
    )

# # Used this endpoint to test tokens. Remember this api is a standalone login api, it does nothing else. Protected endpoints will in YOUR backend. The backend of your app
# @router.get("/protected")
# async def protected(jwt: str = Depends(verify_access_token)):
#     return api_response(success=True, data={"jwt": jwt}, message="ACCESS GRANTED")
