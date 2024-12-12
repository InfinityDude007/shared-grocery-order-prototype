from fastapi import APIRouter
from .supermarket_api import supermarket_router
from .routers import users_router, orders_router

api_router = APIRouter()
api_router.include_router(supermarket_router, prefix="/supermarket/product", tags=["Supermarket API"])
api_router.include_router(users_router, prefix="/users", tags=["Users API"])
api_router.include_router(orders_router, prefix="/orders", tags=["Orders API"])