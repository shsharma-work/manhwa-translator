"""
Base controller with common functionality for all controllers.
"""
from typing import Any, Dict, Optional
from fastapi import HTTPException, status
from app.core.logging import get_logger
from app.core.exceptions import ManhwaTranslatorException

logger = get_logger(__name__)


class BaseController:
    """Base controller with common error handling and response formatting."""
    
    @staticmethod
    def handle_exception(e: Exception, operation: str = "operation") -> HTTPException:
        """Handle exceptions and convert them to appropriate HTTP responses."""
        if isinstance(e, ManhwaTranslatorException):
            logger.warning(f"{operation} failed: {e.message}")
            return HTTPException(
                status_code=e.status_code,
                detail=e.message
            )
        elif isinstance(e, HTTPException):
            logger.warning(f"{operation} failed: {e.detail}")
            return e
        else:
            logger.error(f"Unexpected error during {operation}: {str(e)}")
            return HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error"
            )
    
    @staticmethod
    def create_success_response(data: Any, message: str = "Success") -> Dict[str, Any]:
        """Create a standardized success response."""
        return {
            "success": True,
            "message": message,
            "data": data
        }
    
    @staticmethod
    def create_error_response(message: str, details: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Create a standardized error response."""
        response = {
            "success": False,
            "message": message
        }
        if details:
            response["details"] = details
        return response 