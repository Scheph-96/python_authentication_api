from fastapi import status, HTTPException
from starlette.responses import JSONResponse


class DomainErrors(Exception):
    """
        Base class for all authorization errors.
    """

    code: str = "DOMAIN_ERROR"
    http_status: int = status.HTTP_400_BAD_REQUEST

    def __init__(self, message: str | None = None):
        self.message = message or self.code

    def http(self):
        """
            Convert to JSONResponse
        :return:
        """

        return JSONResponse(
            status_code=self.http_status,
            content={
                "error": self.code,
                "message": self.message
            }
        )
