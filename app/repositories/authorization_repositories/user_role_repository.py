from bson import ObjectId
class UserRolePermission:
    def __init__(self, collection):
        self.collection = collection
        
    def create(self, data: dict):
        result = await self.collection.insert_one(data)
        return result.inserted_id
    
    async def find_by_role_id(self, role_id: str):
        return await self.collection.find_one({"role_id": ObjectId(role_id)})
    
    async def find_by_user_id(self, user_id: str):
        return await self.collection.find_one({"user_id": ObjectId(user_id)})
    
    async def find_by_id(self, user_role_id: str):
        return await self.collection.find_one({"_id": ObjectId(user_role_id)})
    
    async def update(self, user_role_id: str, data: dict):
        await self.collection.update_one({"_id": ObjectId(user_role_id)}, {"$set": data})
        
    async def delete(self, user_role_id: str):
        await self.collection.delete_one({"_id": ObjectId(user_role_id)})