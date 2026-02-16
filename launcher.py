from app.core.config import Settings
import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "app.main:my_app",
        host="0.0.0.0",
        port=8000,
        access_log=False,
        log_level="warning",
        reload=Settings.ENV != "production"
    )