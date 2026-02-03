from fastapi import APIRouter, Depends, BackgroundTasks
from app.schemas.user_schema import UserSignUpSchema, UserSignInSchema, UserLogOutSchema
from app.schemas.email_validation_code import EmailValidationCodeSubmit, EmailValidationCodeRetry
from app.schemas.refresh_token_schema import RefreshTokenSchema
from app.repositories.user_repository import UserRepository
from app.repositories.base_repository import BaseRepository
from app.repositories.refresh_token_repository import RefreshTokenRepository
from app.services.auth_service import AuthService
from app.services.user_service import UserService
from app.services.refresh_token_service import RefreshTokenService
from app.database.motor import db
from app.utils.resources import api_response
# from app.utils.jwt import verify_access_token

router = APIRouter(prefix="/users/auth", tags=["users"])


# Dependency: base repository
def get_base_repository():
    return BaseRepository(db.email_validation_code)

# Dependency: user repository
def get_user_repository():
    return UserRepository(db.users)


# Dependency: refreshToken repository
def get_refresh_token_repository():
    return RefreshTokenRepository(db.refresh_tokens)


# Dependency: user service
def get_user_service(repo: UserRepository = Depends(get_user_repository), base_repo: BaseRepository = Depends(get_base_repository)):
    return UserService(repo, base_repo)


# Dependency: refreshToken service
def get_refresh_token_service(
    repo: RefreshTokenRepository = Depends(get_refresh_token_repository),
):
    return RefreshTokenService(repo)


# Dependency: auth
def get_auth_service(
    user_service: AuthService = Depends(get_user_service),
    refresh_token: RefreshTokenService = Depends(get_refresh_token_service), base_repo: BaseRepository = Depends(get_base_repository)
):
    return AuthService(user_service, refresh_token, base_repo)


"""
    This endpoint create users account
"""
@router.post("/register", response_model=dict)
async def create_user(
    user: UserSignUpSchema,  background_tasks: BackgroundTasks, service: UserService = Depends(get_user_service)
):
    
    user_id = await service.create_user(user.model_dump(), background_tasks)
    return api_response(
        success=True, data={"user_id": user_id}, message="User created successfully"
    )


"""
    This endpoint authenticate our users
"""
@router.post("/login", response_model=dict)
async def get_user(
    user: UserSignInSchema, auth: AuthService = Depends(get_auth_service)
):
    
    auth_token = await auth.login(user.model_dump())

    return api_response(success=True, data=auth_token)

"""
    This endpoint verify users account when they provide the validation code that was sent to their email address
"""
@router.post("/validate_email", response_model=dict)
async def validate_email(data: EmailValidationCodeSubmit, auth: AuthService = Depends(get_auth_service)):
    
    result = await auth.validate_email(data.model_dump())
    
    return api_response(success=True, data=result)

"""
    In case the account validation email was not sent (for any reason), this endpoint ensure the retry process
"""
@router.post("/validate_email/retry", response_model=dict)
async def retry(data: EmailValidationCodeRetry, background_tasks: BackgroundTasks, auth: AuthService = Depends(get_auth_service)):
    
    result = await auth.resend_validate_email(data.model_dump(), background_tasks)
    
    return api_response(success=True, message=result)

"""
    Refresh users access token with the provided refresh token, a new access token is generated with the refresh token
"""
@router.post("/refresh")
async def refresh_token(refresh_token: RefreshTokenSchema, refresh_token_service: RefreshTokenService = Depends(get_refresh_token_service)):
    new_tokens = await refresh_token_service.refresh(refresh_token)
    
    return api_response(success="True", message="New Token Generated", data=new_tokens)

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
