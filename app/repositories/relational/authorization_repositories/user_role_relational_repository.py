from uuid import UUID

from sqlalchemy import select, delete

from app.database.relationnal.relational_db import app_execute_and_fetch_all, app_execute
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

    async def get_user_ids_by_role_id(self, role_id: str):
        pass

    async def get_users_and_permissions(self, user_ids: list):
        pass
