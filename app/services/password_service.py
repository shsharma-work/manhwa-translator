"""
Password service for password hashing and verification.
"""
from passlib.context import CryptContext
from app.core.logging import get_logger

logger = get_logger(__name__)


class PasswordService:
    """Password service for hashing and verifying passwords."""
    
    def __init__(self):
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    
    def hash_password(self, password: str) -> str:
        """Hash a password using bcrypt."""
        try:
            return self.pwd_context.hash(password)
        except Exception as e:
            logger.error(f"Error hashing password: {str(e)}")
            raise ValueError(f"Failed to hash password: {str(e)}")
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify a password against its hash."""
        try:
            return self.pwd_context.verify(plain_password, hashed_password)
        except Exception as e:
            logger.error(f"Error verifying password: {str(e)}")
            return False 