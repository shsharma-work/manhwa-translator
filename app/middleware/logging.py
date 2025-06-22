"""
Logging middleware for request/response logging.
"""
import time
import logging
from typing import Callable
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from app.core.logging import get_logger

logger = get_logger(__name__)


class LoggingMiddleware(BaseHTTPMiddleware):
    """Middleware for logging HTTP requests and responses."""
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """Process the request and log details."""
        start_time = time.time()
        
        # Log request
        logger.info(
            f"Request: {request.method} {request.url.path} "
            f"from {request.client.host if request.client else 'unknown'}"
        )
        
        # Process request
        response = await call_next(request)
        
        # Calculate processing time
        process_time = time.time() - start_time
        
        # Log response
        logger.info(
            f"Response: {response.status_code} "
            f"took {process_time:.4f}s"
        )
        
        # Add processing time to response headers
        response.headers["X-Process-Time"] = str(process_time)
        
        return response 