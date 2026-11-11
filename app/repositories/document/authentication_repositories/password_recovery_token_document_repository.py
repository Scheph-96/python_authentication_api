from uuid import UUID

from app.repositories.document.base_document_repository import BaseDocumentRepository
from app.repositories.interfaces.authentication_repositories_interfaces.password_recovery_token_repository_interface import \
    PasswordRecoveryTokenRepositoryInterface


class PasswordRecoveryTokenDocumentRepository(BaseDocumentRepository, PasswordRecoveryTokenRepositoryInterface):

    async def find_by_hash(self, token_hash: str):
        return await self._collection.find_one({
            "token_hash": token_hash
        })

    async def find_by_user_id(self, user_id: UUID):
        return await self._collection.find_one({
            "user_id": user_id
        })

    async def revoke_password_recovery_token(self, password_recovery_token_id: UUID):
        await self._collection.update_one(
            {
            "_id": password_recovery_token_id
            },
            {
                "$set": {
                    "revoked": True
                }
            }
        )

    async def revoke_all_password_recovery_tokens_by_user_id(self, user_id: UUID):
        await self._collection.update_many(
            {
                "user_id": user_id
            },
            {
                "$set": {
                    "revoked": True
                }
            }
        )
