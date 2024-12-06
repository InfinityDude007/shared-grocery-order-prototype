from sqlalchemy.ext.asyncio import AsyncSession
from .database import session

"""
Function Overview:
Fetch new database session for asynchronous database operations.

Function Logic:
1. Create asynchronous database session.
2. Yield session, allowing for calling function to use it for querying the database.
3. Once the function finishes, session is automatically closed, ensuring proper resource management.

Returns:
- db_session (AsyncSession): The session object yielded to calling function for database interaction.
"""
async def fetch_db_session():
    async with session() as db_session:
        yield db_session