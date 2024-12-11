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

"""
Test Overview:
Establishes an async connection to the database and runs queries to gather and count all rows in a database table.

Test logic:
1. Parameterize the test with tables and their expected row counts.
2. Create an async session using the sessionmaker.
3. Execute query to fetch all rows from specified table and count number of rows returned.
4. Check if row count matches expected value for that table.
5. Yields result to the test function

Returns:
- Yields a boolean indicating if row count matches expected value, along with table, expected row count, and actual row count.
- If query fails, a pytest failure is raised with an error message.
"""
@pytest.fixture(scope="module")
@pytest.mark.parametrize("table,expected_rows", [
    (SupermarketProducts, 20),
    # continue adding new tables here
])
async def query_db(table, expected_rows):
    async with Session() as session:
        try:
            query_result = await session.execute(select(table))
            rows = query_result.scalars().all()
            rows_count = len(rows)
            check_rows = rows_count == expected_rows
            yield check_rows, table, expected_rows, rows_count 
        except OperationalError as e:
            pytest.fail(f"Database connection failed: {e}")

"""
Test Overview:
Validates that tables in the database are populated with the expected number of rows,
using parameterization to check tables and their expected row counts.

Test logic:
1. Use query_db fixture to execute query and check the row count for each specified table.
2. Check bool returned by query_db fixture, and return corresponding message.

Parameters:
- table: Table model being queried.
- expected_rows: Expected number of rows for table being queried.

Returns:
-  A message detailing if table passed check, or if it failed and why.
"""
@pytest.mark.asyncio
async def test_table_population(query_db):
    check_rows, table, expected_rows, rows_count = query_db
    assert check_rows, (
            f"Table '{table.__name__}' should have {expected_rows} rows, but check found {rows_count} rows.")
    print (f"Table '{table.__name__}' has the expected {expected_rows} rows.")
