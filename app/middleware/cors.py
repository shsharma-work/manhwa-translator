"""
CORS middleware configuration.
"""
from typing import List
from app.core.config import settings


def get_cors_config() -> dict:
    """
    Get CORS configuration.
    
    Returns:
        Dictionary with CORS configuration
    """
    return {
        "allow_origins": settings.server.cors_origins,
        "allow_credentials": settings.server.cors_allow_credentials,
        "allow_methods": settings.server.cors_allow_methods,
        "allow_headers": settings.server.cors_allow_headers,
    } 