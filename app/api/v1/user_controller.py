from fastapi import APIRouter, Depends
from app.schemas.user_schema import UserSignUpSchema, UserSignInSchema, UserLogOutSchema
from app.schemas.refresh_token_schema import RefreshTokenSchema
from app.repositories.user_repository import UserRepository
from app.repositories.refresh_token_repository import RefreshTokenRepository
from app.services.auth_service import AuthService
from app.services.user_service import UserService
from app.services.refresh_token_service import RefreshTokenService
from app.database.motor import db
from app.utils.resources import api_response
from app.utils.jwt import verify_access_token

router = APIRouter(prefix="/users/auth", tags=["users"])


# Dependency: repository
def get_user_repository():
    return UserRepository(db.users)


# Dependency: refreshToken
def get_refresh_token_repository():
    return RefreshTokenRepository(db.refresh_tokens)


# Dependency: service
def get_user_service(repo: UserRepository = Depends(get_user_repository)):
    return UserService(repo)


# Dependency: refreshToken
def get_refresh_token_service(
    repo: RefreshTokenRepository = Depends(get_refresh_token_repository),
):
    return RefreshTokenService(repo)


# Dependency: auth
def get_auth_service(
    user_service: AuthService = Depends(get_user_service),
    refresh_token: RefreshTokenService = Depends(get_refresh_token_service),
):
    return AuthService(user_service, refresh_token)


"""
    The endpoint that will register users
"""
@router.post("/auth/register", response_model=dict)
async def create_user(
    user: UserSignUpSchema, service: UserService = Depends(get_user_service)
):
    user_id = await service.create_user(user.model_dump())
    return api_response(
        success=True, data={"id": user_id}, message="User created successfully"
    )


"""
    The endpoint that will log users in
"""
@router.post("/login", response_model=dict)
async def get_user(
    user: UserSignInSchema, auth: AuthService = Depends(get_auth_service)
):
    auth_token = await auth.login(user.model_dump())

    return api_response(success=True, data=auth_token)

"""
    The endpoint that refresh tokens
"""
@router.post("/refresh")
async def refresh_token(refresh_token: RefreshTokenSchema, refresh_token_service: RefreshTokenService = Depends(get_refresh_token_service)):
    new_tokens = await refresh_token_service.refresh(refresh_token)
    
    return api_response(success="True", message="New Token Generated", data=new_tokens)

# @router.get("/protected")
# async def protected(user_id: str = Depends(verify_access_token)):
#     return api_response(success=True, data={"user_id": user_id}, message="ACCESS GRANTED")

# """
#     The endpoint that will log users out
# """
# @router.post("/auth/logout", response_model=dict)
# async def logout(user: UserLogOutSchema, service: UserService = Depends(get_user_service)):
#     try:
#         pass
#     except:
#         return api_response(success=False, message="Unexpected error. Please try again later")
