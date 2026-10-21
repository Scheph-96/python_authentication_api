from sqlalchemy import text
from sqlalchemy.engine import Result
from sqlalchemy.engine import make_url
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.sql import Executable

from app.core.config import Settings
from app.core.logging.logger import get_logger

logger = get_logger("startup")
app_async_engine = create_async_engine(Settings.RELATIONAL_DATABASE_URI, echo=False)

async_local_session = async_sessionmaker(bind=app_async_engine, expire_on_commit=False)


async def init_relational_database():
    """
        Initialize relational database
    """
    database_url = make_url(Settings.RELATIONAL_DATABASE_URI)
    database_name = database_url.database

    # Commit to the maintenance database instead.
    maintenance_url = database_url.set(database="postgres")

    engine = create_async_engine(
        maintenance_url,
        isolation_level="AUTOCOMMIT",
    )

    try:
        async with engine.connect() as connection:
            # Find the database
            result = await connection.execute(
                text("SELECT 1 FROM pg_database WHERE datname = :name"),
                {"name": database_name},
            )

            # If the database does not exist we create it
            if result.scalar_one_or_none() is None:
                logger.info("Database doesn't exist")
                logger.info("Creating database...")
                await connection.exec_driver_sql(
                    f'CREATE DATABASE "{database_name}"'
                )
                logger.info("Database created successfully")
            else:
                logger.info("Database exist")
    finally:
        # Release the connection to the test engine
        await engine.dispose()

    # Verify the target database using your existing application engine,
    async with app_async_engine.connect() as connection:
        logger.info("Establishing connection...")
        await connection.execute(text("SELECT 1"))


async def _exec_query(statement: Executable, commit: bool = False, data: list = None) -> Result:
    """
        Centralizing query execution
    """
    async with async_local_session() as session:
        result = await session.execute(statement, data)

        if commit:
            await session.commit()

    return result


async def app_execute_and_fetch_one(statement: Executable) -> dict:
    """
        Execute a query and return one row
    """
    result = await _exec_query(statement)
    row = result.fetchone()
    return dict(row._mapping)


async def app_execute_and_fetch_all(statement: Executable) -> list:
    """
        Execute the query and return every row that match the query
    """
    result = await _exec_query(statement)
    rows = result.fetchall()
    return [dict(row._mapping) for row in rows]


async def app_execute(statement: Executable) -> Result:
    """
        Execute queries with no row returned
    """
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
