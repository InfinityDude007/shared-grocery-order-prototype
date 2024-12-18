import asyncpg
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
import os
from dotenv import load_dotenv
from .models import BaseModel, SupermarketProducts, Users, Orders, CostSplitting, Accommodation
from .models import hardcoded_products, hardcoded_users, hardcoded_orders, hardcoded_cost_splittings, hardcoded_accommodations
import logging

logger=logging.getLogger(__name__)

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
   In this step, perviously created tables will all be dropped and recreated to ensure any changes from pervious app instances
   do not cause issues.
"""
async def create_database():
    logger.info("Connecting to the PostgreSQL database to check if it exists.")
    connection = await asyncpg.connect(user=USERNAME, password=PASSWORD, host=HOST, port=PORT, database="postgres")
    try:
        db_created = await connection.fetchval("SELECT EXISTS(SELECT 1 FROM pg_database WHERE datname=$1)", NAME)
        if not db_created:
            await connection.execute(f"CREATE DATABASE {NAME}")
            print(f"New database '{NAME}' created.")
        else:
            print(f"The database '{NAME}' already exists. Skipping creation.")
    finally:
        await connection.close()
    
    logger.info("Creating all tables from 'models'.")
    async with async_engine.begin() as db_connection:
        await db_connection.run_sync(BaseModel.metadata.drop_all)
        await db_connection.run_sync(BaseModel.metadata.create_all)
    logger.info("All tables created successfully.")


"""
Function Overview:
Inserts a list of hardcoded product data into SupermarketProducts table.

Function Logic:
1. Open a new database session using provided session.
2. For each product in hardcoded product list, create a new SupermarketProducts record.
3. Add each new product to the database session.
4. Commit session to persist the changes.

Parameters:
session (AsyncSession): The database session used to interact with the database.
"""
async def insert_product_data(session):
    logger.info("Inserting hardcoded product data into SupermarketProducts table.")
    async with session() as db_session:
        for product in hardcoded_products:
            db_session.add(SupermarketProducts(**product))
        await db_session.commit()
        print("Hardcoded product data inserted into SupermarketProducts table.")
        
        
"""
Function Overview:
Inserts a list of hardcoded user data into Users table.

Function Logic:
1. Open a new database session using provided session.
2. For each user in hardcoded user list, create a new Users record.
3. Add each new user to the database session.
4. Commit session to persist the changes.

Parameters:
session (AsyncSession): The database session used to interact with the database.
"""
async def insert_user_data(session):
    logger.info("Inserting hardcoded user data into Users table.")
    async with session() as db_session:
        for user in hardcoded_users:
            db_session.add(Users(**user))
        await db_session.commit()
        print("Hardcoded user data inserted into Users table.")
        

"""
Function Overview:
Inserts a list of hardcoded order data into Orders table.

Function Logic:
1. Open a new database session using provided session.
2. For each order in hardcoded orders list, create a new Orders record.
3. Add each new order to the database session.
4. Commit session to persist the changes.

Parameters:
session (AsyncSession): The database session used to interact with the database.
"""
async def insert_order_data(session):
    logger.info("Inserting hardcoded order data into Orders table.")
    async with session() as db_session:
        for order in hardcoded_orders:
            order["order_total"] = order["items_cost"] + order["delivery_fee"]
            db_session.add(Orders(**order))
        await db_session.commit()
        print("Hardcoded order data inserted into Orders table.")


"""
Function Overview:
Inserts a list of hardcoded cost splitting data into CostSplitting table.

Function Logic:
1. Open a new database session using provided session.
2. For each order in hardcoded cost splitting list, create a new CostSplitting record.
3. Add each new order to the database session.
4. Commit session to persist the changes.

Parameters:
session (AsyncSession): The database session used to interact with the database.
"""
async def insert_cost_splitting_data(session):
    logger.info("Inserting hardcoded cost splitting data into CostSplitting table.")
    async with session() as db_session:
        for cost_split in hardcoded_cost_splittings:
            db_session.add(CostSplitting(**cost_split))
        await db_session.commit()
        print("Hardcoded cost splitting data inserted into CostSplitting table.")

"""
Function Overview:
Inserts a list of hardcoded accommodation data into Accommodation table.

Function Logic:
1. Open a new database session using provided session.
2. For each order in hardcoded accommodation list, create a new Accommodation record.
3. Add each new order to the database session.
4. Commit session to persist the changes.

Parameters:
session (AsyncSession): The database session used to interact with the database.
"""
async def insert_accommodation_data(session):
    logger.info("Inserting hardcoded accommodation data into Accommodation table.")
    async with session() as db_session:
        for accommodation in hardcoded_accommodations:
            db_session.add(Accommodation(**accommodation))
        await db_session.commit()
        print("Hardcoded accommodation data inserted into Accommodation table.")   

"""
Function Overview:
Sets up database by inserting hardcoded data into SupermarketProducts table.

Function Logic:
1. Use async engine context to begin an interaction.
2. Call insert_product_data function to insert predefined data into database.
"""
async def setup_database():
    logger.info("Setting up the database by inserting hardcoded data.")
    async with async_engine.begin():
        await insert_product_data(session)
        await insert_user_data(session)
        await insert_order_data(session)
        await insert_cost_splitting_data(session)
        await insert_accommodation_data(session)
