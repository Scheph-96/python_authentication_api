import uvicorn

from app.core.config import Settings

if __name__ == "__main__":
    uvicorn.run(
        "app.main:my_app",
        host=Settings.APP_HOST,
        port=Settings.APP_PORT,
        access_log=False,
        log_level="warning",
        reload=Settings.ENV != "production"
    )