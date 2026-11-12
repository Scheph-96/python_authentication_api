from sqlalchemy import select

from app.database.relationnal.relational_db import app_execute_and_fetch_one
from app.repositories.interfaces.authorization_repositories_interfaces.role_repository_interface import \
    RoleRepositoryInterface
from app.repositories.relational.base_relational_repository import BaseRelationalRepository
from app.utils.resources import build_sql_expression_from_dict


class RoleRepository(BaseRelationalRepository, RoleRepositoryInterface):
    async def find_by_name(self, role_name: str):
        expression = build_sql_expression_from_dict({"role_name": role_name})
        return await app_execute_and_fetch_one(
            select(self._collection)
            .where(*expression)
        )
