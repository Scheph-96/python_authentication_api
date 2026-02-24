from app.services.model_schema_services.role_service import RoleService
from app.services.model_schema_services.permission_service import PermissionService

class AuthorizationService:
    def __init__(self, role_service: RoleService, permission_service: PermissionService):
        self.role_service = role_service,
        self.permission_service = permission_service
    
    def assign_role(self):
        pass
    
    def assign_permission_to_role(self):
        pass
    
    async def _recompute_permission(self):
        pass