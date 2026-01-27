from fastapi import APIRouter, Depends
from app.schemas.user_schema import UserSignUpSchema, UserSignInSchema, UserLogOutSchema
from app.repositories.user_repository import UserRepository
from app.services.auth_service import AuthService
from app.services.user_service import UserService
from app.database.motor import db
from app.utils.ressources import api_response
router = APIRouter(prefix="/users", tags=["users"])

# Dependency: repository
def get_user_repository():
    return UserRepository(db.users)

# Dependency: service
def get_user_service(repo: UserRepository=Depends(get_user_repository)):
    return UserService(repo)

#Dependency: auth
def get_auth_service(user_service: AuthService=Depends(get_user_service)):
    return AuthService(user_service)

"""
    The endpoint that will register users
"""
@router.post("/auth/register", response_model=dict)
async def create_user(user: UserSignUpSchema, service: UserService = Depends(get_user_service)):
    # try:
    user_id = await service.create_user(user.model_dump())
    return api_response(success=True, data={"id": user_id}, message="User created successfully")
    # except:
    #     return api_response(success=False, message="Unexpected error. Please try again later")

"""
    The endpoint that will log users in
"""
@router.post("/auth/login", response_model=dict)
async def get_user(user: UserSignInSchema, auth: AuthService = Depends(get_auth_service)):
    # try:
    auth_token = await auth.login(user.model_dump())
    
    return api_response(success=True, data=auth_token)
    # except Exception as e:
    #     print(e)
    #     return api_response(success=False, message="Unexpected error. Please try again later")
    
# """
#     The endpoint that will log users out
# """
# @router.post("/auth/logout", response_model=dict)
# async def logout(user: UserLogOutSchema, service: UserService = Depends(get_user_service)):
#     try:
#         pass
#     except:
#         return api_response(success=False, message="Unexpected error. Please try again later")