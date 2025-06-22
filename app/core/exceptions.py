"""
Custom exceptions for the Manhwa Translator API.
"""
from typing import Any, Dict, Optional


class ManhwaTranslatorException(Exception):
    """Base exception for Manhwa Translator API."""
    
    def __init__(
        self,
        message: str,
        status_code: int = 500,
        details: Optional[Dict[str, Any]] = None
    ):
        self.message = message
        self.status_code = status_code
        self.details = details or {}
        super().__init__(self.message)


class AuthenticationError(ManhwaTranslatorException):
    """Raised when authentication fails."""
    
    def __init__(self, message: str = "Authentication failed", details: Optional[Dict[str, Any]] = None):
        super().__init__(message, status_code=401, details=details)


class AuthorizationError(ManhwaTranslatorException):
    """Raised when authorization fails."""
    
    def __init__(self, message: str = "Insufficient permissions", details: Optional[Dict[str, Any]] = None):
        super().__init__(message, status_code=403, details=details)


class ValidationError(ManhwaTranslatorException):
    """Raised when data validation fails."""
    
    def __init__(self, message: str = "Validation error", details: Optional[Dict[str, Any]] = None):
        super().__init__(message, status_code=400, details=details)


class NotFoundError(ManhwaTranslatorException):
    """Raised when a resource is not found."""
    
    def __init__(self, message: str = "Resource not found", details: Optional[Dict[str, Any]] = None):
        super().__init__(message, status_code=404, details=details)


class ConflictError(ManhwaTranslatorException):
    """Raised when there's a conflict (e.g., duplicate resource)."""
    
    def __init__(self, message: str = "Resource conflict", details: Optional[Dict[str, Any]] = None):
        super().__init__(message, status_code=409, details=details)


class DatabaseError(ManhwaTranslatorException):
    """Raised when database operations fail."""
    
    def __init__(self, message: str = "Database error", details: Optional[Dict[str, Any]] = None):
        super().__init__(message, status_code=500, details=details)


class ExternalServiceError(ManhwaTranslatorException):
    """Raised when external service calls fail."""
    
    def __init__(self, message: str = "External service error", details: Optional[Dict[str, Any]] = None):
        super().__init__(message, status_code=502, details=details) 