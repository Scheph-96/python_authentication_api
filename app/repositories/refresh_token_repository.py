from datetime import datetime, timezone
from bson import ObjectId

class RefreshTokenRepository:
    def __init__(self, collection):
        self.collection = collection
        
    async def create(self, refresh_token_entry: dict):
        result = await self.collection.insert_one(refresh_token_entry)
        return result.inserted_id
    
    async def find_by_hash(self, token_hash: str):
        return await self.collection.find_one({"token_hash": token_hash})
    
    async def revoke(self, token_id: str, replaced_by: str = None):
        await self.collection.update_one({"_id": ObjectId(token_id)}, {"$set": {"revoked": True, "replaced_by": replaced_by}})
        
    async def delete_expired_revoked(self):
        await self.collection.delete_many({
            "revoke": True,
            "expires_at": {"$lt": datetime.now(timezone.utc)}
        })