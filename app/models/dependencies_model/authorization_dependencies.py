from fastapi import BackgroundTasks

from app.services.core_services.authentication.model_services.user_service import UserService
from app.services.core_services.authorization.model_services.permission_service import PermissionService
from app.services.core_services.authorization.model_services.role_permission_service import RolePermissionService
from app.services.core_services.authorization.model_services.role_service import RoleService
from app.services.core_services.authorization.model_services.user_role_service import UserRoleService


class AuthorizationDependencies:
    def __init__(self, user_service: UserService, role_service: RoleService, permission_service: PermissionService,
                 role_permission_service: RolePermissionService, user_role_service: UserRoleService,
                 background_tasks: BackgroundTasks):
        self.user_service = user_service
        self.role_service = role_service
        self.permission_service = permission_service
        self.role_permission_service = role_permission_service
        self.user_role_service = user_role_service
        self.background_tasks = background_tasks
