from fastapi import APIRouter

from .tasks_controller import router as tasks_router
from .users_controller import router as users_router

api_router = APIRouter()
api_router.include_router(users_router)
api_router.include_router(tasks_router)
