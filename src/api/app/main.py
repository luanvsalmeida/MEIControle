from contextlib import asynccontextmanager
from typing import Union

from fastapi import FastAPI
from api.db.session import init_db
from api.events import router as event_router
from api.auth import router as auth_router
from api.chat.routing.chat import router as chat_router
from api.chat.routing.message import router as message_router
from api.flows.routing.inflow import router as inflow_router
from api.flows.routing.outflow import router as outflow_router
from api.subscription.routing import router as sub_router
@asynccontextmanager
async def lifespan(app: FastAPI):
    # before app startup up
    init_db()
    yield
    # clean up


app = FastAPI(lifespan=lifespan)
app.include_router(event_router, prefix='/api/events')
app.include_router(auth_router, prefix='/api/auth')
app.include_router(chat_router, prefix='/api/chat')
app.include_router(message_router, prefix='/api/message')
app.include_router(inflow_router, prefix='/api/inflow')
app.include_router(outflow_router, prefix='/api/outflow')
app.include_router(sub_router, prefix='/api/subscription')

# /api/events


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.get("/healthz")
def read_api_health():
    return {"status": "ok"}