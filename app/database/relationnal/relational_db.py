from sqlalchemy import text
from sqlalchemy.engine import Result
from sqlalchemy.engine import make_url
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.sql import Executable

from app.core.config import Settings
from app.core.logging.logger import get_logger
from app.database.relationnal.tables.authentication_sql import init_authentication_tables
from app.database.relationnal.tables.authorization_sql import init_authorization_tables

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

    # Verify the target database using application engine
    async with app_async_engine.connect() as connection:
        logger.info("Establishing connection...")
        await connection.execute(text("SELECT 1"))


async def create_tables():
    """
        Creating tables
    """
    init_authentication_tables()
    init_authorization_tables()

    async with app_async_engine.begin() as connection:
        await connection.run_sync(Settings.SQLALCHEMY_METADATA.create_all)


async def _exec_query(statement: Executable, data: list = None) -> Result:
    """
        Centralizing query execution
    """
    async with async_local_session() as session:
        try:
            result = await session.execute(statement, data)
            await session.commit()
            return result
        except Exception:
            # If the operation failed, discard every previous action
            await session.rollback()
            raise


async def app_execute_and_fetch_one(statement: Executable) -> dict:
    """
        Execute a query and return one row
    """
    result = await _exec_query(statement)
    # result.mappings() changes the format of the returned rows; it doesn't retrieve them
    # mappings() changes row access to mapping-style access.
    # one() expects exactly one row.
    row = result.mappings().one()
    # We could have simply returned the variable 'rows' since RowMapping implements
    # Python's Mapping interface; however, within the app, we work with dictionaries
    # hence the conversion
    return dict(row)


async def app_execute_and_fetch_all(statement: Executable) -> list:
    """
        Execute the query and return every row that match the query
    """
    result = await _exec_query(statement)
    # result.mappings() changes the format of the returned rows; it doesn't retrieve them
    # mappings() changes row access to mapping-style access.
    # all() retrieves all remaining rows into a list.
    rows = result.mappings().all()
    # We could have simply returned the variable 'rows' since RowMapping implements
    # Python's Mapping interface; however, within the app, we work with dictionaries
    # hence the conversion
    return [dict(row) for row in rows]


async def app_execute(statement: Executable) -> Result:
    """
        Execute queries with no row returned.
        Usually inserts, updates and deletes
    :param statement: the SQL query to execute
    """
    result = await _exec_query(statement=statement)
    return result


async def app_execute_many(statement: Executable, data: list) -> Result:
    """
        Execute bulk query. Insert, update and delete
    :param statement: the SQL query to execute
    :param data: the data that will affect the database
    :return:
    """
    result = await _exec_query(statement=statement, data=data)
    return result
