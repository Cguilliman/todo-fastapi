from fastapi import APIRouter
from .auth import router as auth_routers
from .board import router as board_routers


routes = APIRouter()
API_PREFIX = "/api/v1"
routes.include_router(board_routers, prefix=API_PREFIX+"/board")
routes.include_router(auth_routers, prefix=API_PREFIX+"/auth")
