from motor.motor_asyncio import AsyncIOMotorClient

from app.core.config import Settings

# Using motor for non-blocking database operations
client = AsyncIOMotorClient(
    Settings.DATABASE_URI,
            uuidRepresentation="standard" # This line define the binary encoding for uuids
        )
db = client[Settings.DATABASE_NAME]
