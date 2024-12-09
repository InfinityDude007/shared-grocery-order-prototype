from fastapi import FastAPI
from contextlib import asynccontextmanager
from .api import api_router
from .database import create_database, setup_database

"""
Function Overview:
Lifecycle manager for the FastAPI application, used for setting up resources before the application starts.

Function Logic:
1. Wait for the database to be created before starting the application.
2. Yield control back to FastAPI to start the app, ensuring setup is completed first.
"""
@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_database()
    await setup_database()
    yield


# create FastAPI app instance and pass lifespan context manager for proper resource management
app = FastAPI(lifespan=lifespan)


# include the main API router into FastAPI app instance under "Main API Routes" tag for organisation.
app.include_router(api_router, tags=["Main API Routes"])


"""
Endpoint Overview:
Test route to verify if the FastAPI application is running correctly.

Function Logic:
1. The endpoint responds with a simple JSON message indicating that the route was called successfully.

Returns:
- A dictionary with a success message (FastAPI will automatically serialize this to a JSON response).
# Return a dictionary that FastAPI will automatically serialize to JSON
"""
@app.get('/')
async def read_root():
    return {
        "response": "Test route was called successfully.",
        "app_status": "Running."
        }
