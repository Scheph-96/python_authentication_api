from uuid import UUID

from sqlalchemy import Table

from app.database.relationnal.db_r import app_execute, app_execute_many, app_execute_and_fetch_one, \
    app_execute_and_fetch_all
from app.repositories.interfaces.base_repository_interface import BaseRepositoryInterface
from app.utils.resources import build_sql_expression_from_dict


# noinspection PyProtectedMember
class BaseRelationalRepository(BaseRepositoryInterface):

    def __init__(self, collection: Table):
        super().__init__(collection)

    async def create(self, data: dict):
        result = await app_execute(Table.insert(self._collection).values(**data))
        return result.inserted_primary_key[0]

    async def create_many(self, data: list):
        result = await app_execute_many(Table.insert(self._collection), data)
        return result.rowcount

    async def find(self, data: dict):
        expression = build_sql_expression_from_dict(self._collection, data)
        return await app_execute_and_fetch_one(Table.select(self._collection).where(*expression))

    async def find_by_id(self, id: str):
        return await app_execute_and_fetch_one(Table.select(self._collection).where(self._collection.columns._id == UUID(id)))

    async def find_all(self):
        return await app_execute_and_fetch_all(Table.select(self._collection))

    async def update(self, id: str, data: dict):
        await app_execute(Table.update(self._collection).where(self._collection.columns._id == UUID(id)).values(**data))

    async def delete(self, data: dict):
        expression = build_sql_expression_from_dict(self._collection, data)
        await app_execute(Table.delete(self._collection).where(*expression))

    async def delete_one_by_id(self, id: str):
        await app_execute(Table.delete(self._collection).where(self._collection.columns._id == UUID(id)))

    async def delete_many(self, data: dict):
        expression = build_sql_expression_from_dict(self._collection, data)
        await app_execute(Table.delete(self._collection).where(*expression))

    async def delete_many_in(self, ids: list):
        await app_execute(Table.delete(self._collection).where(self._collection.columns._id.in_(ids)))
