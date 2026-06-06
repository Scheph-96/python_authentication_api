from app.core.config import Settings


async def init_indexes(db):

    ####################### UNIQUE INDEXES #######################
    # The "1" stand for the order of sorting. 1 Ascending order -1 Descending order
    # token_hash must be unique
    await db[f"{Settings.USERS_COLLECTION}"].create_index({"email": 1}, unique=True)
    await db[f"{Settings.USERS_COLLECTION}"].create_index({"username": 1}, unique=True)
    await db[f"{Settings.REFRESH_TOKENS_COLLECTION}"].create_index({"token_hash": 1}, unique=True)
    await db[f"{Settings.ROLES_COLLECTION}"].create_index({"role_name": 1}, unique=True)
    await db[f"{Settings.ROLE_PERMISSIONS_COLLECTION}"].create_index([("role_id", 1), ("permission_id", 1)], unique=True)
    await db[f"{Settings.USER_ROLES_COLLECTION}"].create_index([("user_id", 1), ("role_id", 1)], unique=True)

    ####################### EXPIRATION INDEXES #######################
    # Delete the document as soon as the date stored in that field is reached.
    # current_time >= expire_at
    # expireAfterSeconds=0. Delete time is exactly the time set in the document
    await db[f"{Settings.REFRESH_TOKENS_COLLECTION}"].create_index({"expire_at": 1}, expireAfterSeconds=0)
    await db[f"{Settings.EMAIL_VALIDATION_CODE_COLLECTION}"].create_index({"expire_at": 1}, expireAfterSeconds=0)
    await db[f"{Settings.PASSWORD_RECOVERY_TOKENS_COLLECTION}"].create_index({"expire_at": 1}, expireAfterSeconds=0)

    ####################### LOOKUP INDEXES #######################
    # Without an index Mongo does a collection scan (checks every document).
    # With an index Mongo uses a pointer structure to jump directly to matches,
    # which accelerate find queries
    """
        The collection
        {key1: value1, key2: value2} -> doc1
        {key1: value3, key2: value4} -> doc2
        {key1: value5, key2: value6} -> doc3
        {key1: value1, key2: value7} -> doc4
        
        While creating an index on an attribute 
        for example in this case
            `(db.collection.create_index("key1": 1))`
        mongodb create something like this:
        
        value1-  [doc1, doc4]
        value3-  doc2
        value5-  doc3
        
        When a `find` query is done, instead of looking
        for each document in the collection, mongodb
        jump to indexes and resolve the query by just
        picking the corresponding index
    """
    await db[f"{Settings.REFRESH_TOKENS_COLLECTION}"].create_index({"user_id": 1})
    await db[f"{Settings.ROLE_PERMISSIONS_COLLECTION}"].create_index({"role_id": 1})
    await db[f"{Settings.ROLE_PERMISSIONS_COLLECTION}"].create_index({"permission_id": 1})
    await db[f"{Settings.USER_ROLES_COLLECTION}"].create_index({"user_id": 1})
    await db[f"{Settings.USER_ROLES_COLLECTION}"].create_index({"role_id": 1})