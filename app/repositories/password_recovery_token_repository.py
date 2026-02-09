from bson import ObjectId

class PasswordRecoveryTokenRepository:
    def __init__(self, collection):
        self.collection = collection
        
    async def create(self, password_recovery_entry: dict):
        result = await self.collection.insert_one(password_recovery_entry)
        
    async def find_by_hash(self, token_hash: str):
        return await self.collection.find_one({"token_hash": token_hash})
    
    async def find_by_user_id(self, user_id: str):
        return await self.collection.find_one({"_id": ObjectId(user_id)})
    
    async def invalidate_token(self, recovery_token_id: str):
        await self.collection.update_one({"_id": ObjectId(recovery_token_id)}, {"$set": {"used": True}})
        
    async def delete(self, recovery_token_id: str):
        await self.collection.delete_one({"_id": ObjectId(recovery_token_id)})