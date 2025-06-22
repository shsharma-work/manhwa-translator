"""
Security utilities for the Manhwa Translator API.
"""
import secrets
import string
from typing import Optional
from app.core.logging import get_logger

logger = get_logger(__name__)


def generate_secure_token(length: int = 32) -> str:
    """
    Generate a secure random token.
    
    Args:
        length: Length of the token
        
    Returns:
        Secure random token
    """
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))


def generate_api_key() -> str:
    """
    Generate a secure API key.
    
    Returns:
        Secure API key
    """
    return f"mt_{generate_secure_token(48)}"


def hash_sensitive_data(data: str) -> str:
    """
    Hash sensitive data for logging.
    
    Args:
        data: Data to hash
        
    Returns:
        Hashed data
    """
    if len(data) <= 4:
        return "*" * len(data)
    return data[:2] + "*" * (len(data) - 4) + data[-2:]


def validate_api_key(api_key: str) -> bool:
    """
    Validate API key format.
    
    Args:
        api_key: API key to validate
        
    Returns:
        True if valid format, False otherwise
    """
    if not api_key.startswith("mt_"):
        return False
    
    if len(api_key) != 51:  # "mt_" + 48 characters
        return False
    
    # Check if it contains only valid characters
    valid_chars = string.ascii_letters + string.digits
    return all(c in valid_chars for c in api_key[3:]) 