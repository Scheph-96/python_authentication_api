from sqlalchemy import Table, Column, Uuid, String, DateTime, func, ForeignKey, UniqueConstraint, Index
from app.core.config import Settings


def role_table():
    return Table(
        f"{Settings.ROLES_COLLECTION}",
        Settings.SQLALCHEMY_METADATA,
        Column("_id", Uuid, primary_key=True, unique=True, nullable=False),
        Column("role_name", String, nullable=False, unique=True),
        Column("description", String, nullable=True, unique=False),
        Column("created_at", DateTime(timezone=True), server_default=func.now()),
        Index("idx_role", "role_name"),
    )


def permission_table():
    return Table(
        f"{Settings.PERMISSIONS_COLLECTION}",
        Settings.SQLALCHEMY_METADATA,
        Column("_id", Uuid, primary_key=True, unique=True, nullable=False),
        Column("permission_name", String, nullable=False, unique=True),
        Column("created_at", DateTime(timezone=True), server_default=func.now()),
        Index("idx_permission", "permission_name"),
    )


def role_permission_table():
    return Table(
        f"{Settings.ROLE_PERMISSIONS_COLLECTION}",
        Settings.SQLALCHEMY_METADATA,
        Column("_id", Uuid, primary_key=True, unique=True, nullable=False),
        Column("role_id", Uuid, ForeignKey(f"{Settings.ROLES_COLLECTION}._id"), nullable=False),
        Column("permission_id", Uuid, ForeignKey(f"{Settings.PERMISSIONS_COLLECTION}._id"), nullable=False),
        Column("created_at", DateTime(timezone=True), server_default=func.now()),
        UniqueConstraint("role_id", "permission_id", name="unique_role_permission"),
        Index("idx_role_permission_permission", "permission_id"),
        Index("idx_role_permission", "role_id", "permission_id") # Order matter
    )


def user_role_table():
    return Table(
        f"{Settings.USER_ROLES_COLLECTION}",
        Settings.SQLALCHEMY_METADATA,
        Column("_id", Uuid, primary_key=True, unique=True, nullable=False),
        Column("user_id", Uuid, ForeignKey(f"{Settings.USERS_COLLECTION}._id"), nullable=False),
        Column("role_id", Uuid, ForeignKey(f"{Settings.ROLES_COLLECTION}._id"), nullable=False),
        Column("created_at", DateTime(timezone=True), server_default=func.now()),
        UniqueConstraint("user_id", "role_id", name="unique_user_role"),
        Index("idx_user_role_role", "role_id"),
        Index("idx_user_role", "user_id", "role_id") # Order matter
    )
