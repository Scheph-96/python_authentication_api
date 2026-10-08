from app.repositories.interfaces.authentication_repositories_interfaces.password_recovery_token_repository_interface import \
    PasswordRecoveryTokenRepositoryInterface
from app.repositories.relational.base_relational_repository import BaseRelationalRepository


class PasswordRecoveryTokenRelationalRepository(BaseRelationalRepository, PasswordRecoveryTokenRepositoryInterface):
    async def find_by_hash(self, token_hash: str):
        pass

    async def find_by_user_id(self, user_id: str):
        pass

    async def invalidate_token(self, recovery_token_id: str):
        pass