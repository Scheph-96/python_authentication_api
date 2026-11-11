from uuid import UUID

from sqlalchemy import select, update

from app.database.relationnal.relational_db import app_execute_and_fetch_one, app_execute
from app.repositories.interfaces.authentication_repositories_interfaces.password_recovery_token_repository_interface import \
    PasswordRecoveryTokenRepositoryInterface
from app.repositories.relational.base_relational_repository import BaseRelationalRepository
from app.utils.resources import build_sql_expression_from_dict


class PasswordRecoveryTokenRelationalRepository(BaseRelationalRepository, PasswordRecoveryTokenRepositoryInterface):
    async def find_by_hash(self, token_hash: str):
        expression = build_sql_expression_from_dict(self._collection, {"token_hash": token_hash})
        return await app_execute_and_fetch_one(
            select(self._collection)
            .where(*expression)
        )

    async def find_by_user_id(self, user_id: UUID):
        expression = build_sql_expression_from_dict(self._collection, {"user_id": user_id})
        return await app_execute_and_fetch_one(
            select(self._collection)
            .where(*expression)
        )

    async def revoke_password_recovery_token(self, password_recovery_token_id: UUID):
        await app_execute(
            update(self._collection)
            .where(self._collection.columns._id == password_recovery_token_id)
            .values({
                "revoked": True
            })
        )

    async def revoke_all_password_recovery_tokens_by_user_id(self, user_id: UUID):
        await app_execute(
            update(self._collection)
            .where(self._collection.columns.user_id == user_id)
            .values({
                "revoked": True
            })
        )

