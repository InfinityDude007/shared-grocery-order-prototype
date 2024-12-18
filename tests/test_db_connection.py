import os
import pytest
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError
from sqlalchemy.sql import text

# load environment variables, extract database connection parameters and construct database URL
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
Function Overview:
Establishes an async connection to the database and runs a simple query
to verify if the database is accessible and the connection is functional.

Logic logic:
1. Create an async session using the sessionmaker.
2. Execute basic query to test if connection to the database is successful.
3. If query executes successfully, the fixture yields the result to the test function.
4. If query fails due, the fixture fails the test and provides an error message.

Returns:
- If connection is successful, it returns the result to the test.
- If connection fails, it raises a pytest failure and includes the error message from the exception.
"""
async def connect_to_db():
    async with Session() as session:
        try:
            query_result = await session.execute(text('SELECT 1'))
            return query_result 
        except OperationalError as e:
            pytest.fail(f"Database connection failed: {e}")

"""
Test Overview:
Checks if database connection establised by the connect_to_db() fixture is valid.

Test logic:
1. Checks that the session object provided by connect_to_db() is not None, confirming that the connection to the database was established.

Parameters:
- connect_to_db: An async session object used for database interaction.

Returns:
- Implicitly returns a pass or fail based on the assertion.
"""
@pytest.mark.asyncio
async def test_db_connection():
    query_result = await connect_to_db()
    assert query_result is not None
    print("Database connection successful!")
