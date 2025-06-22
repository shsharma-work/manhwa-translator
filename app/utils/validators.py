"""
Utility validators for the Manhwa Translator API.
"""
import re
from typing import Optional
from app.core.logging import get_logger

logger = get_logger(__name__)


def validate_email(email: str) -> bool:
    """
    Validate email format.
    
    Args:
        email: Email address to validate
        
    Returns:
        True if valid, False otherwise
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def validate_username(username: str) -> bool:
    """
    Validate username format.
    
    Args:
        username: Username to validate
        
    Returns:
        True if valid, False otherwise
    """
    # Username must be 3-50 characters, alphanumeric + underscore
    pattern = r'^[a-zA-Z0-9_]{3,50}$'
    return bool(re.match(pattern, username))


def validate_password_strength(password: str) -> tuple[bool, Optional[str]]:
    """
    Validate password strength.
    
    Args:
        password: Password to validate
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"
    
    if not any(c.isupper() for c in password):
        return False, "Password must contain at least one uppercase letter"
    
    if not any(c.islower() for c in password):
        return False, "Password must contain at least one lowercase letter"
    
    if not any(c.isdigit() for c in password):
        return False, "Password must contain at least one digit"
    
    return True, None


def sanitize_input(text: str) -> str:
    """
    Sanitize user input to prevent injection attacks.
    
    Args:
        text: Text to sanitize
        
    Returns:
        Sanitized text
    """
    # Remove potentially dangerous characters
    dangerous_chars = ['<', '>', '"', "'", '&', ';', '(', ')', '{', '}']
    for char in dangerous_chars:
        text = text.replace(char, '')
    
    # Remove extra whitespace
    text = ' '.join(text.split())
    
    return text.strip() 