from fastapi import APIRouter
from .supermarket_api import router as supermarket_router

router = APIRouter()

router.include_router(supermarket_router, tags="Supermarket")