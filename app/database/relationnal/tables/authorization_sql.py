from sqlalchemy import Table, Column, Uuid, String, DateTime, func, ForeignKey
from app.core.config import Settings


def role_table():
    return Table(
        f"{Settings.ROLES_COLLECTION}",
        Settings.SQLALCHEMY_METADATA,
        Column("_id", Uuid, primary_key=True, unique=True, nullable=False),
        Column("role_name", String, nullable=False, unique=True),
        Column("description", String, nullable=True, unique=False),
        Column("created_at", DateTime(timezone=True), server_default=func.now())
    )


def permission_table():
    return Table(
        f"{Settings.PERMISSIONS_COLLECTION}",
        Settings.SQLALCHEMY_METADATA,
        Column("_id", Uuid, primary_key=True, unique=True, nullable=False),
        Column("permission_name", String, nullable=False, unique=False),
        Column("created_at", DateTime(timezone=True), server_default=func.now())
    )


def role_permission_table():
    return Table(
        f"{Settings.ROLE_PERMISSIONS_COLLECTION}",
        Settings.SQLALCHEMY_METADATA,
        Column("_id", Uuid, primary_key=True, unique=True, nullable=False),
        Column("role_id", Uuid, ForeignKey(f"{Settings.ROLES_COLLECTION}"), nullable=False),
        Column("permission_id", Uuid, ForeignKey(f"{Settings.PERMISSIONS_COLLECTION}"), nullable=False),
        Column("created_at", DateTime(timezone=True), server_default=func.now())
    )


def user_role_table():
    return Table(
        f"{Settings.USER_ROLES_COLLECTION}",
        Settings.SQLALCHEMY_METADATA,
        Column("_id", Uuid, primary_key=True, unique=True, nullable=False),
        Column("user_id", Uuid, ForeignKey(f"{Settings.USERS_COLLECTION}"), nullable=False),
        Column("role_id", Uuid, ForeignKey(f"{Settings.ROLES_COLLECTION}"), nullable=False),
        Column("created_at", DateTime(timezone=True), server_default=func.now())
    )
