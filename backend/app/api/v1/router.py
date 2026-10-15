from fastapi import APIRouter
from app.api.v1 import auth, menus, items

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(auth.router)
api_router.include_router(menus.router)
api_router.include_router(items.router)