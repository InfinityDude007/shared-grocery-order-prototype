from fastapi import APIRouter
from .users_routers import router as users_router
from .orders_routers import router as orders_router
from .cost_splitting_routers import router as cost_splitting_router

router = APIRouter()
router.include_router(users_router, tags="Users")
router.include_router(orders_router, tags="Orders")