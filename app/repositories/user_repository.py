from bson import ObjectId

class UserRepository:
    def __init__(self, collection):
        self.collection = collection
        
    async def find_by_email(self, email: str):
        return await self.collection.find_one({"email": email})
    
    async def find_by_username(self, username: str):
        return await self.collection.find_one({"username": username})
    
    async def create(self, data: dict):
        result = await self.collection.insert_one(data)
        return str(result.inserted_id)
    
    async def find_by_id(self, user_id: str):
        return await self.collection.find_one({"_id": ObjectId(user_id)})
    
    async def update(self, user_id: str, data: dict):
        await self.collection.update_one({"_id": ObjectId(user_id)}, {"$set": data})
        
    async def update_inc(self, user_id: str, data: dict):
        await self.collection.update_one({"_id": ObjectId(user_id)}, {"$inc": data})
        
    async def delete(self, user_id: str):
        await self.collection.delete_one({"_id": ObjectId(user_id)})
    