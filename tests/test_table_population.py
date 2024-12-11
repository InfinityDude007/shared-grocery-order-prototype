import os
import pytest
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.future import select
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
async def db_session():
    async with Session() as session:
        yield session

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
async def test_table_population(db_session, table, expected_rows):
    query = select(table)
    query_result = await db_session.execute(query)
    rows = query_result.scalars().all()
    rows_count = len(rows)
    if rows_count == expected_rows:
        print(f"Table '{table.__name__}' has the expected {expected_rows} rows.")
    else:
        assert rows_count == expected_rows, f"Table '{table.__name__}' should have {expected_rows} rows, but the test found {rows_count} rows."
