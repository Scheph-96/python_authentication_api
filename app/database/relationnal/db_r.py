from sqlalchemy.sql import Executable
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from app.core.config import Settings

app_async_engine = create_async_engine("", echo=Settings.ENV == "development")

async_local_session = async_sessionmaker(bind=app_async_engine, expire_on_commit=False)


async def _exec_query(statement: Executable, commit:bool=False, data:list=None) -> Result:
    async with async_local_session() as session:
        result = await session.execute(statement, data)

        if commit:
            await session.commit()

    return result


async def app_execute_and_fetch_one(statement: Executable) -> dict:
    result = await _exec_query(statement)
    row = result.fetchone()
    return dict(row._mapping)


async def app_execute_and_fetch_all(statement: Executable) -> list:
    result = await _exec_query(statement)
    rows = result.fetchall()
    return [dict(row._mapping) for row in rows]


async def app_execute(statement: Executable) -> Result:
    result = await _exec_query(statement=statement, commit=True)
    return result

async def app_execute_many(statement: Executable, data: list) -> Result:
    """
        Mostly for bulk insertion
    :param statement:
    :param data:
    :return:
    """
    result = await _exec_query(statement=statement, data=data, commit=True)
    return result
