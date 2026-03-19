from fastapi import APIRouter, BackgroundTasks
from fastapi.params import Depends

from app.api.v1.authentication_controller import get_user_service
from app.core.config import Settings
from app.database.motor import db
from app.models.dependencies_model.authorization_dependencies import AuthorizationDependencies
from app.repositories.authorization_repositories.permission_repository import PermissionRepository
from app.repositories.authorization_repositories.role_permission_repository import RolePermissionRepository
from app.repositories.authorization_repositories.role_repository import RoleRepository
from app.repositories.authorization_repositories.user_role_repository import UserRoleRepository
from app.schemas.authorization_schema.role_schema import AssignRoleSchema, CreateRoleSchema, RemoveUserRoleSchema
from app.services.core_services.authentication.model_services.user_service import UserService
from app.services.core_services.authorization.authorization_service import AuthorizationService
from app.services.core_services.authorization.model_services.permission_service import PermissionService
from app.services.core_services.authorization.model_services.role_permission_service import RolePermissionService
from app.services.core_services.authorization.model_services.role_service import RoleService
from app.services.core_services.authorization.model_services.user_role_service import UserRoleService
from app.utils.resources import api_response

router = APIRouter(prefix=f"{Settings.API_PREFIX}/authorize")


########################################### DEPENDENCIES ###########################################


# Dependency: role repository
def get_role_repository():
    return RoleRepository(db.roles)


# Dependency: permission repository
def get_permission_repository():
    return PermissionRepository(db.permissions)


# Dependency: rolePermission repository
def get_role_permission_repository():
    return RolePermissionRepository(db.role_permissions)


# Dependency: userRole repository
def get_user_role_repository():
    return UserRoleRepository(db.user_roles)


# Dependency: role service
def get_role_service(repo: RoleRepository = Depends(get_role_repository)):
    return RoleService(repo)


# Dependency: permission service
def get_permission_service(repo: PermissionRepository = Depends(get_permission_repository)):
    return PermissionService(repo)


# Dependency: rolePermission service
def get_role_permission_service(repo: RolePermissionRepository = Depends(get_role_permission_repository)):
    return RolePermissionService(repo)


# Dependency: userRole service
def get_user_role_service(repo: UserRoleRepository = Depends(get_user_role_repository)):
    return UserRoleService(repo)


# Dependency: authorization service
def get_autho_service(
        background_tasks: BackgroundTasks,
        user_service: UserService = Depends(get_user_service),
        role_service: RoleService = Depends(get_role_service),
        permission_service: PermissionService = Depends(get_permission_service),
        role_permission_service: RolePermissionService = Depends(get_role_permission_service),
        user_role_service: UserRoleService = Depends(get_user_role_service),
):
    return AuthorizationService(
        AuthorizationDependencies(user_service=user_service, role_service=role_service, permission_service=permission_service,
                                  role_permission_service=role_permission_service, user_role_service=user_role_service,
                                  background_tasks=background_tasks)
    )

########################################### ENDPOINTS ###########################################

@router.post("/create_role", response_model=dict)
async def create_role(create_role_schema: CreateRoleSchema, authorization_service: AuthorizationService = Depends(get_autho_service)):
    result = await authorization_service.create_role(create_role_schema.model_dump())

    return api_response(data=result, message="Role Created Successfully")

@router.post("/assign_role", response_model=dict)
async def assign_role(assign_role_schema: AssignRoleSchema, authorization_service: AuthorizationService = Depends(get_autho_service)):
    result = await authorization_service.assign_role_to_user(assign_role_schema.model_dump())

    return api_response(data=result, message="Role Assigned Successfully")

@router.post("/remove_user_role", response_model=dict)
async def remove_user_role(remove_user_role_schema: RemoveUserRoleSchema, authorization_service: AuthorizationService = Depends(get_autho_service)):
    result = await authorization_service.remove_user_role(remove_user_role_schema.model_dump())

    return api_response(data=result, message="Role Removed Successfully")

