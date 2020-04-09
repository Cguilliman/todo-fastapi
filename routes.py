from fastapi import APIRouter
from rest.routers import router as board_routers


routes = APIRouter()


routes.include_router(board_routers, prefix="/api/v1")
