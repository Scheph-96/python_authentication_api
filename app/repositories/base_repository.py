from bson import ObjectId

class BaseRepository:
    def __init__(self, collection):
        self.collection = collection
        
    async def create(self, data: dict):
        result = await self.collection.insert_one(data)
        return str(result.inserted_id)
    
    async def find_by_id(self, id: str):
        return await self.collection.find_one({"_id": ObjectId(id)})
    
    async def find(self, data: dict):
        return await self.collection.find_one(data)
    
    async def update(self, id: str, data: dict):
        await self.collection.update_one({"_id": ObjectId(id)}, {"$set": data})
        
    async def delete(self, id: str):
        await self.collection.delete_one({"_id": ObjectId(id)})