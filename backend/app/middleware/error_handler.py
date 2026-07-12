"""Global error handling middleware."""

from fastapi import Request
from fastapi.responses import JSONResponse
from loguru import logger


class APIError(Exception):
    """Base API exception."""

    def __init__(
        self,
        message: str,
        code: str = "API_ERROR",
        status_code: int = 400,
    ):
        self.message = message
        self.code = code
        self.status_code = status_code


class ValidationError(APIError):
    def __init__(self, message: str):
        super().__init__(
            message=message,
            code="VALIDATION_ERROR",
            status_code=400,
        )


class AuthenticationError(APIError):
    def __init__(self, message: str):
        super().__init__(
            message=message,
            code="AUTHENTICATION_ERROR",
            status_code=401,
        )


class NotFoundError(APIError):
    def __init__(self, resource: str):
        super().__init__(
            message=f"{resource} not found",
            code="NOT_FOUND",
            status_code=404,
        )


async def global_exception_handler(
    request: Request,
    exc: Exception,
):
    request_id = getattr(
        request.state,
        "request_id",
        "unknown",
    )

    if isinstance(exc, APIError):
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": exc.code,
                "message": exc.message,
                "request_id": request_id,
            },
        )

    logger.exception(exc)

    return JSONResponse(
        status_code=500,
        content={
            "error": "INTERNAL_SERVER_ERROR",
            "message": "An unexpected error occurred",
            "request_id": request_id,
        },
    )