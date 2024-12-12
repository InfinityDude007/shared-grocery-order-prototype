import os
import pytest
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, close_all_sessions
from sqlalchemy.future import select
from sqlalchemy.exc import OperationalError
from server.models import SupermarketProducts, Users, Orders # continue adding new tables here

# load environment variables, extract database connection parameters and construct database URL
USERNAME = os.getenv('DATABASE_USER')
PASSWORD = os.getenv('DATABASE_PASSWORD')
HOST = os.getenv('DATABASE_HOST')
PORT = os.getenv('DATABASE_PORT')
NAME = os.getenv('DATABASE_NAME')
URL = f"postgresql+asyncpg://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{NAME}"

# create asynchronous engine and sessionmaker binded to it for interacting with the database
async_engine = create_async_engine(URL, echo=True, pool_size=5, pool_pre_ping=True)  # adjust pool_size as tables are added

@pytest.fixture(scope="function")
async def new_session():
    test_session = sessionmaker(async_engine, class_=AsyncSession, expire_on_commit=False)
    async with test_session() as connection:
        yield connection

@pytest.mark.asyncio
@pytest.mark.parametrize("table,expected_rows", [
    (SupermarketProducts, 20),
    (Users, 20),
    (Orders, 15)
    # continue adding new tables here
])
async def test_table_population(new_session, table, expected_rows):
    try:
        query_result = await new_session.execute(select(table))
        rows = query_result.scalars().all()
        rows_count = len(rows)
        check_rows = rows_count == expected_rows
        assert check_rows, (f"Table '{table.__tablename__}' should have {expected_rows} rows, but check found {rows_count} rows.")
        print (f"Table '{table.__tablename__}' has the expected {expected_rows} rows.")
    except OperationalError as e:
        pytest.fail(f"Database connection failed: {e}")
    except Exception as e:
        pytest.fail(f"An error occurred within the test script: {e}")

@pytest.fixture(scope="session", autouse=True)
async def dispose_engine():
    yield
    await async_engine.dispose()
