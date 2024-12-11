import os
import pytest
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.future import select
from sqlalchemy.exc import OperationalError
from dotenv import load_dotenv
from server.models import BaseModel, SupermarketProducts # continue adding new tables here

# load environment variables, extract database connection parameters and construct database URL
load_dotenv()
USERNAME = os.getenv('DATABASE_USER')
PASSWORD = os.getenv('DATABASE_PASSWORD')
HOST = os.getenv('DATABASE_HOST')
PORT = os.getenv('DATABASE_PORT')
NAME = os.getenv('DATABASE_NAME')
URL = f"postgresql+asyncpg://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{NAME}"

# create asynchronous engine and sessionmaker binded to it for interacting with the database
async_engine = create_async_engine(URL, echo=True)
Session = sessionmaker(async_engine, class_=AsyncSession, expire_on_commit=False)

# set up an async database session fixture to interact with the database and provide the session to test functions
@pytest.fixture(scope="module")
async def connect_to_db():
    async with async_engine.connect() as connection:
        async with Session(bind=connection) as session:
            try:
                await session.execute('SELECT 1')
                yield session
            except OperationalError as e:
                pytest.fail(f"Database connection failed: {e}")

"""
Test Overview:
Validates that tables in database are populated with the expected number of rows,
using parameterization to check tables and expected row counts.

Test logic:
1. Parameterize test with tables and their expected row counts.
2. Execute query to retrieve all rows from each specified table.
3. Compare number of rows in each table to expected number of rows.
4. Raise assertion error if row count does not match expected number of rows.

Parameters:
- table: Table model to query.
- expected_rows: Expected number of rows in table.

Returns:
- Test passes if the row count for each table matches expected value.
- If row count does not match, a pytest assertation error is raised with an error message.
"""
@pytest.mark.asyncio
@pytest.mark.parametrize("table,expected_rows", [
    (SupermarketProducts, 20),
    # continue adding new tables here
])
async def test_table_population(connect_to_db, table, expected_rows):
    try:
        query = select(table)
        query_result = await connect_to_db.execute(query)
        rows = query_result.scalars().all()
        rows_count = len(rows)
        assert rows_count == expected_rows, (
            f"Table '{table.__name__}' should have {expected_rows} rows, "
            f"but check found {rows_count} rows."
        )
        print(f"Table '{table.__name__}' has the expected {expected_rows} rows.")
    except OperationalError as e:
        pytest.fail(f"Failed to query table '{table.__name__}': {e}")
