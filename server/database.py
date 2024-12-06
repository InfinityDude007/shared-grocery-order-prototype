import asyncpg
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
import os
from dotenv import load_dotenv
from .models.base_model import BaseModel

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
session = sessionmaker(bind=async_engine, class_=AsyncSession, expire_on_commit=False)

"""
Function Overview:
Creates the database, first checking if it exists and creating it if not, then creates all (subclass) tables from 'models'.

Function Logic:
1. Connect to the PostgreSQL database server using asyncpg to check if the database exists.
2. If the database does not exist, create it.
3. After ensuring the database exists, create all tables that are subclasses of BaseModel containted in the 'model' folder.
"""
async def create_database():
    connection = await asyncpg.connect(user=USERNAME, password=PASSWORD, host=HOST, port=PORT, database="postgres")
    try:
        db_created = await connection.fetchval("SELECT EXISTS(SELECT 1 FROM pg_database WHERE datname=$1)", NAME)
        if not db_created:
            await connection.execute(f"CREATE DATABASE {NAME}")
            print(f"New database '{NAME}' created.")
        else:
            print(f"The database '{NAME}' already exists. Skipping creation."
)
    finally:
        await connection.close()

    async with async_engine.begin() as db_connection:
        await db_connection.run_sync(BaseModel.metadata.create_all)
