from motor.motor_asyncio import AsyncIOMotorClient
from bson import UuidRepresentation
from app.core.config import settings

# Using motor for non-blocking database operations
client = AsyncIOMotorClient(
            settings.DATABASE_URI,
            uuidRepresentation="standard" # This line define the binary encoding for uuids
        )
db = client[settings.DATABASE_NAME]