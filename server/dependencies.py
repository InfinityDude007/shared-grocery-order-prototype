from sqlalchemy.ext.asyncio import AsyncSession
from .database import SessionLocal

"""
Function Overview:
Fetch new database session for asynchronous database operations.

Function Logic:
1. Create asynchronous database session.
2. Yield session, allowing for calling function to use it for querying the database.
3. Once the function finishes, session is automatically closed, ensuring proper resource management.

Parameters:
- db_session (AsyncSession): The session yielded to calling function for database interaction.

Returns:
- AsyncSession: A session object that can be used to interact with the database asynchronously.
"""
async def fetch_db_session():
    async with SessionLocal() as db_session:
        yield db_session