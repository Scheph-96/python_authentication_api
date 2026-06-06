from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from app.core.logging.logger import get_logger

"""
    Project Exceptions Configuration
"""
class ExceptionConfig:
    def __init__(self, my_app: FastAPI):
        self.logger = get_logger("code_log")
        
        my_app.add_exception_handler(HTTPException, self.http_exception_handler)
        my_app.add_exception_handler(Exception, self.unhandled_exception_handler)

    """     
        When this runs:
        raise HTTPException(400, "Any Error")
        
        The handler transform it into:
        HTTP/1.1 400 Bad Request
        Content-Type: application/json

        {"detail": "Any Error"}

    """
    async def http_exception_handler(self, request: Request, exc: HTTPException):
        # This is the format of what we see in logs
        self.logger.info(
            "BusinessException",
            path=request.url.path,
            method=request.method,
            status_code=exc.status_code,
            detail=exc.detail,
            client=request.client.host
        )
        
        # This JSONResponse becomes the HTTP response sent to the client
        return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})
        
    """
        Logging format of any other Exception raised in our code
        
        unhandled_exception_handler only works inside
        HTTP request → FastAPI router → response cycle
    """
    async def unhandled_exception_handler(self, request: Request, exc: Exception):
        self.logger.error(
            "UnhandledException",
            path=request.url.path,
            method=request.method,
            error=str(exc),
            exc_info=True,
        )
        
        return JSONResponse(status_code=500, content={"detail": "Something went wrong. Please try again later!"})
