import os
import pytest
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.future import select
from sqlalchemy.exc import OperationalError
from server.models import SupermarketProducts, Users, Orders, CostSplitting, Accommodation

# load environment variables, extract database connection parameters and construct database URL
USERNAME = os.getenv('DATABASE_USER')
PASSWORD = os.getenv('DATABASE_PASSWORD')
HOST = os.getenv('DATABASE_HOST')
PORT = os.getenv('DATABASE_PORT')
NAME = os.getenv('DATABASE_NAME')
URL = f"postgresql+asyncpg://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{NAME}"

"""
Test Overview:
Verifies that specified database tables contain expected number of rows,
based on hardcoded data to ensure they were populated correctly.

Test logic:
1. Test is parameterized to create multiple test instances for all tables with their expected row counts.
2. For each table, an async session is created, and a query is executed to fetch all rows from table.
3. The row count is then compared with the expected row count for the table.
4. If the row count doesn't match, the test will fail with an appropriate error message indicating the mismatch.

Parameters:
- table: The table to be tested.
- expected_rows: The expected number of rows in the table.

Returns:
- If row count matches, test passes and prints a success message.
- If row count does not match, test fails and provides an error message with the expected and actual row counts.
"""
@pytest.mark.asyncio
@pytest.mark.parametrize("table,expected_rows", [
    (SupermarketProducts, 20),
    (Users, 20),
    (Orders, 15),
    (CostSplitting, 4),
    (Accommodation, 5)
])
async def test_table_population(table, expected_rows):
    async_engine = create_async_engine(URL, echo=True, pool_size=10, pool_pre_ping=True)  # adjust pool_size as tables are added
    session = sessionmaker(async_engine, class_=AsyncSession, expire_on_commit=False)
    async with session() as test_session:
        try:
            query_result = await test_session.execute(select(table))
            rows = query_result.scalars().all()
            rows_count = len(rows)
            check_rows = rows_count == expected_rows
            assert check_rows, (f"Table '{table.__tablename__}' should have {expected_rows} rows, but check found {rows_count} rows.")
            print (f"Table '{table.__tablename__}' has the expected {expected_rows} rows.")
        except OperationalError as e:
            pytest.fail(f"Database connection failed: {e}")
        except Exception as e:
            pytest.fail(f"An error occurred within the test script: {e}")
