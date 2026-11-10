from datetime import datetime, timezone
from uuid import UUID

from sqlalchemy import select, update, bindparam

from app.database.relationnal.relational_db import app_execute_and_fetch_one, app_execute, app_execute_many
from app.repositories.interfaces.authentication_repositories_interfaces.refresh_token_repository_interface import \
    RefreshTokenRepositoryInterface
from app.repositories.relational.base_relational_repository import BaseRelationalRepository
from app.utils.resources import build_sql_expression_from_dict


class RefreshTokenRelationalRepository(BaseRelationalRepository, RefreshTokenRepositoryInterface):
    async def find_by_hash(self, token_hash: str):
        expression = build_sql_expression_from_dict(self._collection, {"token_hash": token_hash})
        return await app_execute_and_fetch_one(
            select(self._collection)
            .where(*expression)
        )

    async def revoke(self, token_id: UUID, new_refresh_token: str | None = None):
        await app_execute(
            update(self._collection)
            .where(self._collection.columns._id == token_id)
            .values({
                    "revoked": True,
                    "replaced_by": new_refresh_token
                })
        )

    async def revoke_and_expire_all_refresh_tokens_by_user_id(self, user_id: UUID):
        await app_execute(
            update(self._collection)
            .where(self._collection.columns._id == user_id)
            .values({
                    "revoked": True,
                    "expire_at": datetime.now(timezone.utc)
                })
        )

    async def delete_expired_revoked(self):
        pass
