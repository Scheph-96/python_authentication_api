from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.api.v1.user_controller import router as user_router
from app.database.motor import db
from app.database.init_indexes import init_indexes

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load indexes
    # Execute this line before the application start
    await init_indexes(db)
    yield

my_app = FastAPI(lifespan=lifespan)

my_app.include_router(user_router)

@my_app.get("/")
def root():
    return {"status": "ok"}