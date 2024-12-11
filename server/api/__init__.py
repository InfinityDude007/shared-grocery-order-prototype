from fastapi import APIRouter
from .supermarket_api import supermarket_router
from .routers import orders_router

api_router = APIRouter()
api_router.include_router(supermarket_router, prefix="/supermarket", tags=["Supermarket API"])
api_router.include_router(orders_router, prefix="/orders", tags=["Orders API"])