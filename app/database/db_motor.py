from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings

# Using motor for non-blocking database operations
client = AsyncIOMotorClient(settings.MONGO_URI)
db = client[settings.MONGO_DB_NAME]