from fastapi import APIRouter, Depends
from app.schemas.user_schema import UserSignUpSchema, UserSignInSchema, UserLogOutSchema
from app.repositories.user_repository import UserRepository
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

"""
    The endpoint that will register users
"""
@router.post("/auth/register", response_model=dict)
async def create_user(user: UserSignUpSchema, service: UserService = Depends(get_user_service)):
    try:
        user_id = await service.create_user(user.model_dump())
        return api_response(success=True, data={"id": user_id}, message="User created successfully")
    except:
        return api_response(success=False, message="Unexpected error. Please try again later")

"""
    The endpoint that will log users in
"""
@router.post("/auth/login", response_model=dict)
async def get_user(user: UserSignInSchema, service: UserService = Depends(get_user_service)):
    try: 
        user = await service.get_user(user.model_dump())
        
        if user:
            return api_response(data=user, message="User found")
        else:
            return api_response(data=user, message="No User found")
    except:
        return api_response(success=False, message="Unexpected error. Please try again later")
    
"""
    The endpoint that will log users out
"""
@router.post("/auth/logout", response_model=dict)
async def logout(user: UserLogOutSchema, service: UserService = Depends(get_user_service)):
    try:
        pass
    except:
        return api_response(success=False, message="Unexpected error. Please try again later")