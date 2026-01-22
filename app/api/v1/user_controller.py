from fastapi import APIRouter, Depends
from app.schemas.user_schema import UserCreateSchema, UserGetSchema
from app.repositories.user_repository import UserRepository
from app.services.user_service import UserService
from app.database.motor import db
from app.utils.ressources import api_response
from bson import ObjectId

router = APIRouter(prefix="/users", tags=["users"])

# Dependency: repository
def get_user_repository():
    return UserRepository(db.users)

# Dependency: service
def get_user_service(repo: UserRepository=Depends(get_user_repository)):
    return UserService(repo)

@router.post("/", response_model=dict)
async def create_user(user: UserCreateSchema, service: UserService = Depends(get_user_service)):
    user_id = await service.create_user(user.model_dump())
    return api_response(data={"id": user_id}, message="User created successfully")

@router.post("/auth", response_model=dict)
async def get_user(user: UserGetSchema, service: UserService = Depends(get_user_service)):
    user = await service.get_user(user.model_dump())
    
    if user:
        return api_response(data=user, message="User found")
    else:
        return api_response(data=user, message="No User found")