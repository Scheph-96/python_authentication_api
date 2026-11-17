from uuid import UUID

from sqlalchemy import select, delete

from app.database.relationnal.relational_db import app_execute_and_fetch_all, app_execute, app_execute_and_scalars_all
from app.database.relationnal.tables.authorization_sql import permission_table, role_permission_table
from app.repositories.interfaces.authorization_repositories_interfaces.user_role_repository_interface import \
    UserRoleRepositoryInterface
from app.repositories.relational.base_relational_repository import BaseRelationalRepository
from app.utils.resources import build_sql_expression_from_dict


class UserRoleRelationalRepository(BaseRelationalRepository, UserRoleRepositoryInterface):
    async def find_by_role_id(self, role_id: UUID, **kwargs):
        expression = build_sql_expression_from_dict(self._collection, {"role_id": role_id})
        return await app_execute_and_fetch_all(
            select(self._collection)
            .where(*expression)
        )

    async def find_by_user_id(self, user_id: UUID, **kwargs):
        expression = build_sql_expression_from_dict(self._collection, {"user_id": user_id})
        return await app_execute_and_fetch_all(
            select(self._collection)
            .where(*expression)
        )

    async def find_by_user_ids(self, user_ids: list, **kwargs):
        return await app_execute_and_fetch_all(
            select(self._collection)
            .where(self._collection.columns.user_id.in_(user_ids))
        )

    async def delete_many_by_role_id(self, role_id: UUID):
        expression = build_sql_expression_from_dict(self._collection, {"role_id": role_id})
        await app_execute(
            delete(self._collection)
            .where(*expression)
        )

    async def get_user_ids_by_role_id(self, role_id: UUID):
        expression = build_sql_expression_from_dict(self._collection, {"role_id": role_id})
        return await app_execute_and_scalars_all(
            select(self._collection.columns.user_id)
            .where(*expression)
        )

    async def get_users_and_permissions(self, user_ids: list):
        permission = permission_table()
        role_permission = role_permission_table()

        rows = await app_execute_and_scalars_all(
            # Retrieve the user_id column from user_role collection
            # and permission_name from permission collection
            select(
                self._collection.columns.user_id,
                permission.columns.permission_name
            )
            # join user_role collection with role_permission collection
            # on role_id
            .join(
                role_permission,
                role_permission.columns.role_id == self._collection.columns.role_id
            )
            # join permission collection with role_permission collection
            # on permission_id
            .join(
                permission,
                permission.columns._id == role_permission.columns.permission_id
            )
            # ids to look for user_role collection
            .where(self._collection.columns.user_id.in_(user_ids))
        )

        users_permissions = {}

        """
            If this user ID doesn't exist in the dictionary yet,
            create an entry for it with an empty set.
            Otherwise, leave its existing value unchanged.
    
            Suppose the first row is:
            {
                "user_id": "user_1",
                "permission_name": "user:read"
            }
    
            Initially:
            users_permissions = {}
    
            We execute:
            users_permissions.setdefault("user_1", set())
    
            The dictionary becomes:
            {"user_1": set()}
    
            Then:
            users_permissions["user_1"].add("user:read")
    
            Result:
            {"user_1": {"user:read"}}
        """
        for row in rows:
            users_permissions.setdefault(row["user_id"], set()).add(
                row["permission_name"]
            )

        """
            Converting this {"user_1": {"user:read"}} to
            {"user_1": ["user:read"]}
        """
        users_permissions = [
            {
                "user_id": user_id,
                "permission": list(permissions)
            }
            for user_id, permissions in users_permissions.items()
        ]

        return users_permissions




















