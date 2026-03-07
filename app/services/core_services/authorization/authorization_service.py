from app.core.logging.logger import get_logger
from app.models.dependencies_model.authorization_dependencies import AuthorizationDependencies
from app.services.core_services.authorization.model_services.permission_service import PermissionService
from app.services.core_services.authorization.model_services.role_service import RoleService


class AuthorizationService:
    def __init__(self, autho_depends: AuthorizationDependencies):
        self.autho_depends = autho_depends
        self.logger = get_logger("AuthorizationService")
    
    def assign_role(self):
        pass
    
    def assign_permission_to_role(self):
        pass
    
    async def _recompute_permission(self):
        pass