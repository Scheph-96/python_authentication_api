from uuid import UUID

import collections
from sqlalchemy import select, delete

from app.database.relationnal.relational_db import app_execute_and_fetch_one, app_execute_and_fetch_all, app_execute
from app.database.relationnal.tables.authorization_sql import user_role_table
from app.repositories.interfaces.authorization_repositories_interfaces.role_permission_repository_interface import \
    RolePermissionRepositoryInterface
from app.repositories.relational.base_relational_repository import BaseRelationalRepository
from app.utils.resources import build_sql_expression_from_dict


class RolePermissionRelationalRepository(BaseRelationalRepository, RolePermissionRepositoryInterface):
    async def find_by_role_id(self, role_id: UUID):
        expression = build_sql_expression_from_dict(self._collection, {"role_id": role_id})
        return await app_execute_and_fetch_all(
            select(self._collection)
            .where(*expression)
        )

    async def find_by_role_ids(self, role_ids: list, **kwargs):
        return await app_execute_and_fetch_all(
            select(self._collection)
            .where(self._collection.columns.role_id.in_(role_ids))
        )

    async def find_by_permission_id(self, permission_id: UUID):
        expression = build_sql_expression_from_dict(self._collection, {"permission_id": permission_id})
        return await app_execute_and_fetch_all(
            select(self._collection)
            .where(*expression)
        )

    async def get_user_ids_from_role_permissions(self, permission_id: UUID):
        """
            Return users that have the provided permission

            Logic
            Find role_permissions matching the permission_id.
            Join with user_roles using role_id.
            Collect unique user_id values.
        """
        expression = build_sql_expression_from_dict(self._collection, {"permission_id": permission_id})
        user_role = user_role_table()

        return await app_execute_and_fetch_all(
            select(user_role.columns.user_id)
            .join(
                self._collection,
                self._collection.columns.role_id == user_role.columns.role_id
            )
            .where(*expression)
            .distinct()
        )

    async def delete_many_by_role_id(self, role_id: UUID):
        expression = build_sql_expression_from_dict(self._collection, {"role_id": role_id})
        await app_execute(
            delete(self._collection)
            .where(*expression)
        )

    async def delete_many_by_permission_id(self, permission_id: UUID):
        expression = build_sql_expression_from_dict(self._collection, {"permission_id": permission_id})
        await app_execute(
            delete(self._collection)
            .where(*expression)
        )
