from typing import TypeVar, Generic

T = TypeVar("T")


class BaseRepositoryInterface(Generic[T]):
    def __init__(self, collection: T):
        self._collection: T = collection

    async def create(self, *args, **kwargs):
        pass

    async def create_many(self, *args, **kwargs):
        pass

    async def find(self, *args, **kwargs):
        pass

    async def find_by_id(self, *args, **kwargs):
        pass

    async def find_all(self, *args, **kwargs):
        pass

    async def update(self, *args, **kwargs):
        pass

    async def delete(self, *args, **kwargs):
        pass

    async def delete_one_by_id(self, *args, **kwargs):
        pass

    async def delete_many(self, *args, **kwargs):
        pass

    async def delete_many_in(self, *args, **kwargs):
        pass
