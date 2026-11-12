from sqlalchemy import select

from app.database.relationnal.relational_db import app_execute_and_fetch_one, app_execute_and_fetch_all
from app.repositories.interfaces.authorization_repositories_interfaces.permission_repository_interface import \
    PermissionRepositoryInterface
from app.repositories.relational.base_relational_repository import BaseRelationalRepository
from app.utils.resources import build_sql_expression_from_dict


class PermissionRelationalRepository(BaseRelationalRepository, PermissionRepositoryInterface):
    async def find_by_name(self, permission_name: str, **kwargs):
        expression = build_sql_expression_from_dict(self._collection, {"permission_name": permission_name})
        return await app_execute_and_fetch_one(
            select(self._collection)
            .where(*expression)
        )

    async def find_by_name_in(self, permissions_names: list, **kwargs):
        return await app_execute_and_fetch_all(
            select(self._collection)
            .where(self._collection.columns.permission_name.in_(permissions_names))
        )

    async def find_by_ids(self, permission_ids: list, **kwargs):
        return await app_execute_and_fetch_all(
            select(self._collection)
            .where(self._collection.columns._id.in_(permission_ids))
        )
