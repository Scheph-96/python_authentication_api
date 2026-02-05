import time
from starlette.middleware.base import BaseHTTPMiddleware
from app.core.logging.logger import get_logger

logger = get_logger("requests")

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        start = time.time()
        response = await call_next(request)
        duration = round((time.time() - start) * 1000, 2)
        
        logger.info(
            "RequestCompleted",
            path=request.url.path,
            method=request.method,
            status_code=response.status_code,
            duration_ms=duration
        )
        
        return response