from fastapi import FastAPI
from starlette.requests import Request
from starlette.responses import Response
from models.base import SessionLocal
from rest.routers.base import routes
from render.routers import router
from ws.consumers import router as ws_router


app = FastAPI()
app.include_router(routes)
app.include_router(router)
app.include_router(ws_router)
# app.mount("/static", StaticFiles(directory="static"), name="static")
# templates = Jinja2Templates(directory="templates")


@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    response = Response("Internal server error", status_code=500)
    try:
        request.state.db = SessionLocal()
        response = await call_next(request)
    finally:
        request.state.db.close()
    return response
