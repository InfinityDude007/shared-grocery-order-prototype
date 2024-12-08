# to be updated with api routes as they are created

from fastapi import APIRouter
from .supermarket_api import supermarket_router

api_router = APIRouter()
api_router.include_router(supermarket_router, prefix="/supermarket", tags=["Supermarket API"])