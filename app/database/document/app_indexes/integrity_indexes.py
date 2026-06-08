from app.core.config import Settings


async def integrity_indexes(db):
    """
    UNIQUE INDEXES
    The "1" stand for the order of sorting. 1 Ascending order -1 Descending order
    token_hash must be unique

    :param db database client instance
    """
    await db[f"{Settings.USERS_COLLECTION}"].create_index({"username": 1}, name="idx_users_integrity_username", unique=True)
    await db[f"{Settings.USERS_COLLECTION}"].create_index({"email": 1}, name="idx_users_integrity_email", unique=True)
    await db[f"{Settings.REFRESH_TOKENS_COLLECTION}"].create_index({"token_hash": 1}, name="idx_rf_token_token_hash", unique=True)
    await db[f"{Settings.PASSWORD_RECOVERY_TOKENS_COLLECTION}"].create_index({"token_hash": 1}, name="idx_pass_recov_token_hash", unique=True)
    await db[f"{Settings.EMAIL_VALIDATION_CODE_COLLECTION}"].create_index({"code_hash": 1}, name="idx_email_valid_code_hash", unique=True)
    await db[f"{Settings.ROLES_COLLECTION}"].create_index({"role_name": 1}, name="idx_roles_integrity_role_name", unique=True)
    await db[f"{Settings.PERMISSIONS_COLLECTION}"].create_index({"permission_name": 1}, name="idx_permissions_integrity_permission_name", unique=True)
    await db[f"{Settings.ROLE_PERMISSIONS_COLLECTION}"].create_index([("role_id", 1), ("permission_id", 1)], name="idx_role_permissions_integrity",
                                                                     unique=True)
    await db[f"{Settings.USER_ROLES_COLLECTION}"].create_index([("user_id", 1), ("role_id", 1)], name="idx_user_roles_integrity", unique=True)
