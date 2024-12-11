from fastapi import APIRouter
from .orders_routers import router as orders_router

router = APIRouter()

router.include_router(orders_router, tags="Orders")