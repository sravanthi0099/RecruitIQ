"""Logging middleware for structured request/response logging."""

import time
import uuid
from typing import Callable

from fastapi import Request, Response
from loguru import logger
from starlette.middleware.base import BaseHTTPMiddleware


class LoggingMiddleware(BaseHTTPMiddleware):
    """Middleware for structured logging of all requests and responses."""

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """Process request and response with logging."""
        # Generate unique request ID
        request_id = str(uuid.uuid4())
        request.state.request_id = request_id

        # Log request
        logger.info(
            "Request received",
            extra={
                "request_id": request_id,
                "method": request.method,
                "path": request.url.path,
                "client": request.client.host if request.client else None,
            },
        )

        # Measure request time
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time

        # Log response
        logger.info(
            "Response sent",
            extra={
                "request_id": request_id,
                "status_code": response.status_code,
                "process_time": f"{process_time:.3f}s",
                "method": request.method,
                "path": request.url.path,
            },
        )

        # Add custom headers
        response.headers["X-Request-ID"] = request_id
        response.headers["X-Process-Time"] = str(process_time)

        return response
