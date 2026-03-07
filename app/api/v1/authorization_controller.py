from fastapi import APIRouter, BackgroundTasks
from fastapi.params import Depends

from app.core.config import Settings
from app.database.motor import db
from app.models.dependencies_model.authorization_dependencies import AuthorizationDependencies
from app.repositories.authorization_repositories.permission_repository import PermissionRepository
from app.repositories.authorization_repositories.role_permission_repository import RolePermissionRepository
from app.repositories.authorization_repositories.role_repository import RoleRepository
from app.repositories.authorization_repositories.user_role_repository import UserRoleRepository
from app.services.core_services.authorization.authorization_service import AuthorizationService
from app.services.core_services.authorization.model_services.permission_service import PermissionService
from app.services.core_services.authorization.model_services.role_permission_service import RolePermissionService
from app.services.core_services.authorization.model_services.role_service import RoleService
from app.services.core_services.authorization.model_services.user_role_service import UserRoleService

router = APIRouter(prefix=f"{Settings.API_PREFIX}/authorize")
background_tasks = BackgroundTasks()


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
        role_service: RoleService = Depends(get_role_service),
        permission_service: PermissionService = Depends(get_permission_service),
        role_permission_service: RolePermissionService = Depends(get_role_permission_service),
        user_role_service: UserRoleService = Depends(get_user_role_service),
):
    return AuthorizationService(
        AuthorizationDependencies(role_service=role_service, permission_service=permission_service,
                                  role_permission_service=role_permission_service, user_role_service=user_role_service,
                                  background_tasks=background_tasks)
    )

########################################### ENDPOINTS ###########################################
