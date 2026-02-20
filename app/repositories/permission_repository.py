from bson import ObjectId

class PermissionRepository:
    def __init__(self, collection):
        self.collection = collection
        
    async def create(self, data: dict):
        result = await self.collection.insert_one(data)
        return result.inserted_id
    
    async def find_by_id(self, permission_id: str):
        return await self.collection.find_one({"_id": ObjectId(permission_id)})
    
    async def update(self, permission_id: str, data: dict):
        await self.collection.update_one({"_id": permission_id}, {"$set": data})
        
    async def delete(self, permission_id: str):
        await self.collecion.delete_one({"_id": permission_id})