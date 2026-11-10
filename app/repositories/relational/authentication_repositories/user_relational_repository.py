from uuid import UUID

from sqlalchemy import select, update, bindparam

from app.database.relationnal.relational_db import app_execute_and_fetch_one, app_execute, app_execute_many
from app.repositories.interfaces.authentication_repositories_interfaces.user_repository_interface import \
    UserRepositoryInterface
from app.repositories.relational.base_relational_repository import BaseRelationalRepository
from app.utils.resources import build_sql_expression_from_dict


class UserRelationalRepository(BaseRelationalRepository, UserRepositoryInterface):
    async def find_by_email(self, email: str):
        expression = build_sql_expression_from_dict(self._collection, {"email": email})
        return await app_execute_and_fetch_one(
            select(self._collection)
            .where(*expression)
        )

    async def find_by_username(self, username: str):
        expression = build_sql_expression_from_dict(self._collection, {"username": username})
        return await app_execute_and_fetch_one(
            select(self._collection)
            .where(*expression)
        )

    async def update_inc_auth_version(self, user_id: UUID):
        await app_execute(
            update(self._collection)
            .where(self._collection.columns._id == user_id)
            .values(auth_version=self._collection.auth_version + 1))

    async def update_many_user(self, user_ids: list, data: dict):
        await app_execute(
            update(self._collection)
            .where(self._collection._id.in_(user_ids)
            .values(**data))
        )

    async def update_users_effective_permissions(self, updates: list):
        """
            Updates user effective permissions by user_id
        :param: updates: A list of objects with this format
        {
            "user_id": <user_is>,
            "permissions": <list of permission>
        }
        """
        await app_execute_many(
            update(self._collection)
            .where(self._collection.c._id == bindparam("user_id"))
            .values({
                "user_id": bindparam("user_id"),
                "effective_permissions": bindparam("user_id")
            }), updates
        )
