from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.v1.authentication_controller import router as authentication_router
from app.api.v1.authorization_controller import router as authorization_router
from app.core.config import Settings
from app.core.errors.domain_errors import DomainErrors
from app.core.exception_config import ExceptionConfig
from app.core.logging.logger import get_logger
from app.core.logging.logging_config import logging_config
from app.database.init_indexes import init_indexes
from app.database.db_motor import db
from app.middleware.logging_middleware import LoggingMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Execute these lines when the application is starting

    # Initialize logging
    logging_config()

    logger = get_logger("startup")
    logger.info("Starting authentication API")
    logger.info(f"Environment: {Settings.ENV}")

    await db.client.admin.command("ping")
    logger.info(f"Database connection established")

    try:
        # Load indexes
        await init_indexes(db)
        logger.info("Database indexes initialized")
    except Exception as e:
        logger.error("Index initialization failed", exc_info=True)
        raise

    logger.info("Application Running")

    yield
    # Execute these lines when the application is stopping
    logger.info("Shutting down authentication API")

my_app = FastAPI(lifespan=lifespan)

ExceptionConfig(my_app)
my_app.add_middleware(LoggingMiddleware)

my_app.include_router(authentication_router)

# Authorization endpoints are accessible only when authorization interface is enabled
if Settings.ACTIVATE_AUTHORIZATION_INTERFACE:
    my_app.include_router(authorization_router)

@my_app.exception_handler(DomainErrors)
async def domain_error_handler(request, exc: DomainErrors):
    return exc.http()


@my_app.get("/")
def root():
    return {"status": "ok"}
