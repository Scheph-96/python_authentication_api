from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.v1.authentication_controller import router as authentication_router
from app.api.v1.authorization_controller import router as authorization_router
from app.core.config import Settings
from app.core.errors.domain_errors import DomainErrors
from app.core.exception_config import ExceptionConfig
from app.core.logging.logger import get_logger
from app.core.logging.logging_config import logging_config
from app.database.document.app_indexes.integrity_indexes import integrity_indexes
from app.database.document.app_indexes.lifecycle_indexes import lifecycle_indexes
from app.database.document.app_indexes.query_indexes import query_indexes
from app.database.document.document_db import document_db
from app.database.relationnal import relational_db
from app.middleware.logging_middleware import LoggingMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Execute these lines when the application is starting

    # Add authentication endpoints
    my_app.include_router(authentication_router)

    # Initialize logging
    logging_config()

    logger = get_logger("startup")
    logger.info("Starting authentication API")
    logger.info(f"Environment: {Settings.ENV}")

    # Database initialization
    if Settings.DATABASE_TYPE == "document":
        # Check document database activity
        # Throw an error when the connection failed
        try:
            await document_db.client.admin.command("ping")
            logger.info("Database connection established successfully")

            try:
                # await drop_all_indexes(db)
                # Load indexes
                await integrity_indexes(document_db)
                await lifecycle_indexes(document_db)
                await query_indexes(document_db)
                logger.info("Database indexes initialized")
            except Exception as e:
                logger.error("Index initialization failed", exc_info=True)
                raise
        except Exception:
            logger.error("Database connection failed")
            raise
    elif Settings.DATABASE_TYPE == "relational":
        # Check database activity
        # Throw an error when the connection failed
        try:
            await relational_db.init_relational_database()
            logger.info("Database connection established successfully")
        except Exception:
            logger.error("Database connection failed")
            raise
    else:
        logger.error("Unsupported database type")
        raise

    # Authorization endpoints are accessible only when authorization interface is enabled
    if Settings.ACTIVATE_AUTHORIZATION_INTERFACE:
        my_app.include_router(authorization_router)
        logger.info("Authorization routes added")

    # SMTP variables must be defined if email validation is enabled
    if Settings.EMAIL_VALIDATION:
        if (not Settings.SMTP_HOST
                or not Settings.SMTP_PORT
                or not Settings.SMTP_USER
                or not Settings.SMTP_PASSWORD
                or not Settings.SMTP_FROM):
            logger.error("SMTP variables are not initialized. Check .env")
            raise

    logger.info(f"Application Running at http://{Settings.APP_HOST}:{Settings.APP_PORT}")

    yield
    # Execute these lines when the application is stopping
    logger.info("Shutting down authentication API")


my_app = FastAPI(lifespan=lifespan)

# Cannot add middleware after an application has started
ExceptionConfig(my_app)
my_app.add_middleware(LoggingMiddleware)

@my_app.exception_handler(DomainErrors)
async def domain_error_handler(request, exc: DomainErrors):
    return exc.http()


@my_app.get("/")
def root():
    return {"status": "ok"}
