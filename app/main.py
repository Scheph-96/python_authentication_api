from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.api.v1.user_controller import router as user_router
from app.core.logging.logging_config import configure_logging
from app.core.exception_config import ExceptionConfig
from app.middleware.logging_middleware import LoggingMiddleware
from app.database.motor import db
from app.database.init_indexes import init_indexes

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Execute these lines before the application start
    # Initialize logging
    configure_logging()
    # Load indexes
    await init_indexes(db)
    yield
    # Execute these lines before the application stop

my_app = FastAPI(lifespan=lifespan)

my_app.include_router(user_router)
ExceptionConfig(my_app)
my_app.add_middleware(LoggingMiddleware)

@my_app.get("/")
def root():
    return {"status": "ok"}