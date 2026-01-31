async def init_indexes(db):
    # token_hash must be unique
    await db.refresh_tokens.create_index({"token_hash": 1}, unique=True)
    # Delete the document as soon as the date stored in that field is reached.
    # current_time >= expire_at
    # expireAfterSeconds=0. Delete time is exactly the time set in the document
    await db.refresh_tokens.create_index({"expire_at": 1}, expireAfterSeconds=0)
    # Without an index → Mongo does a collection scan (checks every document).
    # With an index → Mongo uses a pointer structure to jump directly to matches.
    await db.refresh_tokens.create_index({"user_id": 1})