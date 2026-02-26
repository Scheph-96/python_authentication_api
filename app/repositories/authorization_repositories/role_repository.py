from bson import ObjectId

class RoleRepository:
    def __init__(self, collection):
        self.collection = collection
        
    async def create(self, data: dict):
        result = await self.collection.insert_one(data)
        return result.inserted_id
    
    async def find_by_id(self, role_id: str):
        return await self.collection.find_one({"_id": ObjectId(role_id)})
    
    async def find_by_name(self, role_name: str):
        return await self,collection.find_one({"name": role_name})
    
    async def update(self, role_id: str, updated_data: dict):
        await self.collection.update_one({"_id": ObjectId(role_id)}, {"$set": updated_data})
        
    async def delete(self, role_id: str):
        await self.collection.delete_one({"_id": ObjectId(role_id)})