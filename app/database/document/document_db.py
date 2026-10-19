from motor.motor_asyncio import AsyncIOMotorClient
from bson import UuidRepresentation
from app.core.config import Settings

# Using motor for non-blocking database operations
client = AsyncIOMotorClient(
            Settings.DOCUMENT_DATABASE_URI,
            uuidRepresentation="standard" # This line define the binary encoding for uuids
        )
document_db = client[Settings.DATABASE_NAME]