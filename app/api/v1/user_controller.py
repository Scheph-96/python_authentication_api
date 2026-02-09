from fastapi import APIRouter, Depends, BackgroundTasks
from app.schemas.user_schema import UserSignUpSchema, UserSignInSchema, UserLogOutSchema
from app.schemas.email_validation_code import (
    EmailValidationCodeSubmit,
    EmailValidationCodeRetry,
)
from app.schemas.refresh_token_schema import RefreshTokenSchema
from app.schemas.password_recovery_token_schema import (
    PasswordRecoveryConfirmEmailSchema,
    PasswordRecoveryResetPasswordSchema,
)
from app.repositories.base_repository import BaseRepository
from app.repositories.user_repository import UserRepository
from app.repositories.refresh_token_repository import RefreshTokenRepository
from app.repositories.password_recovery_token_repository import (
    PasswordRecoveryTokenRepository,
)
from app.services.auth_service import AuthService
from app.services.user_service import UserService
from app.services.refresh_token_service import RefreshTokenService
from app.services.password_recovery_token_service import PasswordRecoveryTokenService

from app.database.motor import db
from app.utils.resources import api_response

# from app.utils.jwt import verify_access_token

router = APIRouter(prefix="/users/auth", tags=["users"])


# Check refresh or access token before each login attempt.
# Right now I don't know exactly. You will figure it out


# Dependency: base repository
def get_email_validation_repository():
    return BaseRepository(db.email_validation_code)


# Dependency: user repository
def get_user_repository():
    return UserRepository(db.users)


# Dependency: refreshToken repository
def get_refresh_token_repository():
    return RefreshTokenRepository(db.refresh_tokens)

    return BaseRepository(db.email_validation_code)


# Dependency: passwordRecoveryToken repository
def get_password_recovery_token_repository():
    return PasswordRecoveryTokenRepository(db.password_recovery_token)


# Dependency: user service
def get_user_service(
    repo: UserRepository = Depends(get_user_repository),
    base_repo: BaseRepository = Depends(get_email_validation_repository),
):
    return UserService(repo, base_repo)


# Dependency: refreshToken service
def get_refresh_token_service(
    repo: RefreshTokenRepository = Depends(get_refresh_token_repository),
):
    return RefreshTokenService(repo)


# Dependency: passwordRecovery service
def get_password_recovery_token_service(
    repo: PasswordRecoveryTokenRepository = Depends(
        get_password_recovery_token_repository
    ),
):
    return PasswordRecoveryTokenService(repo)


# Dependency: auth service
def get_auth_service(
    user_service: AuthService = Depends(get_user_service),
    refresh_token: RefreshTokenService = Depends(get_refresh_token_service),
    base_repo: BaseRepository = Depends(get_email_validation_repository),
    password_recovery_token_service: PasswordRecoveryTokenService = Depends(
        get_password_recovery_token_service
    ),
):
    return AuthService(
        user_service, refresh_token, base_repo, password_recovery_token_service
    )


"""
    This endpoint create users account
"""


@router.post("/register", response_model=dict)
async def user_registration(
    user: UserSignUpSchema,
    background_tasks: BackgroundTasks,
    service: UserService = Depends(get_user_service),
):

    user_id = await service.user_registration(user.model_dump(), background_tasks)
    return api_response(
        success=True, data={"user_id": user_id}, message="User created successfully"
    )


"""
    This endpoint authenticate our users
"""


@router.post("/login", response_model=dict)
async def user_login(
    user: UserSignInSchema, auth: AuthService = Depends(get_auth_service)
):

    auth_token = await auth.login(user.model_dump())

    return api_response(success=True, data=auth_token)


"""
    This endpoint verify users account when they provide the validation code that was sent to their email address
"""


@router.post("/validate_email", response_model=dict)
async def validate_email(
    data: EmailValidationCodeSubmit, auth: AuthService = Depends(get_auth_service)
):

    result = await auth.validate_email(data.model_dump())

    return api_response(success=True, data=result)


"""
    In case the account validation email was not sent (for any reason), this endpoint ensure the retry process
"""


@router.post("/validate_email/retry", response_model=dict)
async def retry(
    data: EmailValidationCodeRetry,
    background_tasks: BackgroundTasks,
    auth: AuthService = Depends(get_auth_service),
):

    result = await auth.resend_validate_email(data.model_dump(), background_tasks)

    return api_response(success=True, message=result)


"""
    Refresh users access token with the provided refresh token, a new access token is generated with the refresh token
"""


@router.post("/refresh")
async def refresh_token(
    refresh_token: RefreshTokenSchema,
    auth_service: AuthService = Depends(get_auth_service),
):
    new_tokens = await auth_service.refresh_token(refresh_token.model_dump())

    return api_response(success="True", message="New Token Generated", data=new_tokens)


"""
    We check the email address provided by the user in the password recovery process
"""


@router.post("/password_recovery/forgot")
async def password_forgot(
    password_recovery_confirm_email: PasswordRecoveryConfirmEmailSchema,
    auth: AuthService = Depends(get_auth_service),
):

    password_recovery_token = await auth.password_recovery_confirm_email(
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
    auth: AuthService = Depends(get_auth_service),
):
    result = await auth.password_recovery_reset_password(password_recovery_reset_password.model_dump())
    
    return api_response(
        success= True,
        message= result,
    )


# """
#     The endpoint that will log users out
# """
# @router.post("/auth/logout", response_model=dict)
# async def logout(user: UserLogOutSchema, service: UserService = Depends(get_user_service)):
#     try:
#         pass
#     except:
#         return api_response(success=False, message="Unexpected error. Please try again later")


# Used this endpoint to test tokens. Remember this api is a stand alone login api, it does nothing else. Protected endpoints will in YOUR backend. The backend of your app
# @router.get("/protected")
# async def protected(user_id: str = Depends(verify_access_token)):
#     return api_response(success=True, data={"user_id": user_id}, message="ACCESS GRANTED")
