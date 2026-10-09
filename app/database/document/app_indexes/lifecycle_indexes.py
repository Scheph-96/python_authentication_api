from app.core.config import Settings


async def lifecycle_indexes(db):
    """
    EXPIRATION INDEXES\n
    Delete the document as soon as the date stored in that field is reached.
    current_time >= expire_at\n
    expireAfterSeconds=0. Delete time is exactly the time set in the document\n

    :param db database client instance
    """
    await db[f"{Settings.REFRESH_TOKENS_COLLECTION}"].create_index({"expire_at": 1}, expireAfterSeconds=0)
    await db[f"{Settings.EMAIL_VALIDATION_CODE_COLLECTION}"].create_index({"expire_at": 1}, expireAfterSeconds=0)
    await db[f"{Settings.PASSWORD_RECOVERY_TOKENS_COLLECTION}"].create_index({"expire_at": 1}, expireAfterSeconds=0)