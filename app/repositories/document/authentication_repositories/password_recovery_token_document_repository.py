from uuid import UUID

from app.repositories.document.base_document_repository import BaseDocumentRepository
from app.repositories.interfaces.authentication_repositories_interfaces.password_recovery_token_repository_interface import \
    PasswordRecoveryTokenRepositoryInterface


class PasswordRecoveryTokenDocumentRepository(BaseDocumentRepository, PasswordRecoveryTokenRepositoryInterface):

    async def find_by_hash(self, token_hash: str):
        return await self._collection.find_one({"token_hash": token_hash})

    async def find_by_user_id(self, user_id: str):
        return await self._collection.find_one({"user_id": UUID(user_id)})

    async def invalidate_token(self, recovery_token_id: str):
        await self._collection.update_one({"_id": UUID(recovery_token_id)}, {"$set": {"is_used": True}})
