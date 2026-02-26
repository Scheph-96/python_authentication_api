from bson import ObjectId

class RolePermissionRepository:    
    def __init__(self, collection):
        self.collection = collection
        
    async def create(self, data: dict):
        result = await self.collection.insert_one(data)
        return result.insert_id
    
    async def find_by_role_id(self, role_id: str):
        return await self.collection.find_one({"role_id": ObjectId(role_id)})
    
    async def find_by_permission_id(self, permission_id: str):
        return await self.collection.find_one({"permission_id": ObjectId(permission_id)})
    
    async def find_by_role_permission_id(self, role_permission_id: str):
        return await self.collection.find_one({"_id": ObjectId(role_permission_id)})
    
    async def update(self, role_permission_id: str, data: dict):
        await self.collection.update_one({"_id": ObjectId(role_permission_id)}, {"$set": data})
        
    async def delete(self, role_permission: str):
        await self.collection.delete_one({"_id": ObjectId(role_permission)})