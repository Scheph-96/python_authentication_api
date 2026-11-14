from uuid import UUID

from sqlalchemy import select

from app.database.relationnal.relational_db import app_execute_and_fetch_one, app_execute_and_fetch_all
from app.repositories.interfaces.authorization_repositories_interfaces.role_permission_repository_interface import \
    RolePermissionRepositoryInterface
from app.repositories.relational.base_relational_repository import BaseRelationalRepository
from app.utils.resources import build_sql_expression_from_dict


class RolePermissionRelationalRepository(BaseRelationalRepository, RolePermissionRepositoryInterface):
    async def find_by_role_id(self, role_id: UUID):
        expression = build_sql_expression_from_dict(self._collection, {"role_id": role_id})
        return await app_execute_and_fetch_one(
            select(self._collection)
            .where(*expression)
        )

    async def find_by_role_ids(self, role_ids: list, **kwargs):
        return await app_execute_and_fetch_all(
            select(self._collection)
            .where(self._collection.columns.role_id.in_(role_ids))
        )

    async def find_by_permission_id(self, permission_id: str):
        pass

    async def get_user_ids_from_role_permissions(self, permission_id: str):
        pass

    async def delete_many_by_role_id(self, role_id: str):
        pass

    async def delete_many_by_permission_id(self, permission_id: str):
        pass
