from bson import ObjectId

from app.repositories.base_repository import BaseRepository


class RolePermissionRepository(BaseRepository):
    
    def find_by_role_id(self, role_id: str):
        return self.collection.find({"role_id": ObjectId(role_id)})
    
    def find_by_permission_id(self, permission_id: str):
        return self.collection.find({"permission_id": ObjectId(permission_id)})