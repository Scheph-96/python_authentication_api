from datetime import timezone, datetime, timedelta

from sqlalchemy import Table, Column, Uuid, Integer, String, Boolean, DateTime, func, ForeignKey, Index

from app.core.config import Settings


def user_table():
    return Table(
        f"{Settings.USERS_COLLECTION}",
        Settings.SQLALCHEMY_METADATA,
        Column("_id", Uuid, primary_key=True, unique=True, nullable=False),
        Column("username", String, nullable=True, unique=True),
        Column("email", String, nullable=True, unique=True),
        Column("hashed_password", String, nullable=False),
        Column("auth_version", Integer, nullable=False),
        Column("effective_permissions", String, nullable=False, server_default=""),
        Column("is_verified", Boolean, nullable=False, default=False),
        Column("created_at", DateTime(timezone=True), server_default=func.now()),
        Index("idx_username", "username"),
        Index("idx_email", "email")
    )


def refresh_token_table():
    return Table(
        f"{Settings.REFRESH_TOKENS_COLLECTION}",
        Settings.SQLALCHEMY_METADATA,
        Column("_id", Uuid, primary_key=True, unique=True, nullable=False),
        Column("user_id", Uuid, ForeignKey(f"{Settings.USERS_COLLECTION}._id"), nullable=False),
        Column("token_hash", String, nullable=False, unique=True),
        Column("auth_version", Integer, nullable=False),
        Column("replaced_by", String, nullable=True),
        Column("revoked", Boolean, nullable=False, default=False),
        Column("expire_at", DateTime(timezone=True),
               default=lambda: (datetime.now(timezone.utc) + timedelta(days=Settings.REFRESH_TOKEN_EXPIRATION_DAYS))),
        Column("created_at", DateTime(timezone=True), server_default=func.now()),
        Index("idx_rf_token_user_id", "user_id"),
        Index("idx_rf_token_token_hash", "token_hash")
    )


def password_recovery_token():
    return Table(
        f"{Settings.PASSWORD_RECOVERY_TOKENS_COLLECTION}",
        Settings.SQLALCHEMY_METADATA,
        Column("_id", Uuid, primary_key=True, unique=True, nullable=False),
        Column("user_id", Uuid, ForeignKey(f"{Settings.USERS_COLLECTION}._id")),
        Column("token_hash", String, nullable=False, unique=True),
        Column("expire_at", DateTime(timezone=True), default=lambda: (
                datetime.now(timezone.utc) + timedelta(minutes=Settings.PASSWORD_RECOVERY_TOKEN_EXPIRATION_MINUTES))),
        Column("created_at", DateTime(timezone=True), server_default=func.now()),
        Column("is_used", Boolean, nullable=False, default=False),
        Index("idx_pass_recov_user_id", "user_id"),
        Index("idx_pass_recov_token_hash", "token_hash")
    )


def email_validation_code():
    return Table(
        f"{Settings.EMAIL_VALIDATION_CODE_COLLECTION}",
        Settings.SQLALCHEMY_METADATA,
        Column("_id", Uuid, primary_key=True, unique=True, nullable=False),
        Column("user_id", Uuid, ForeignKey(f"{Settings.USERS_COLLECTION}._id")),
        Column("code_hash", String, nullable=False, unique=True),
        Column("is_used", Boolean, nullable=False, default=False),
        Column("expire_at", DateTime(timezone=True), default=lambda: (
                datetime.now(timezone.utc) + timedelta(hours=Settings.EMAIL_VALIDATION_CODE_EXPIRATION_HOURS))),
        Column("created_at", DateTime(timezone=True), server_default=func.now()),
        Index("idx_email_valid_user_id", "user_id"),
        Index("idx_email_valid_token_hash", "code_hash")
    )
