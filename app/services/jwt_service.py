"""
JWT service for token creation and verification.
"""
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from app.core.config import settings
from app.core.logging import get_logger
from app.models.user import User
from app.schemas.user import Token

logger = get_logger(__name__)


class JWTService:
    """JWT service for token operations."""
    
    def __init__(self):
        self.secret_key = settings.security.secret_key
        self.algorithm = settings.security.algorithm
        self.access_token_expire_minutes = settings.security.access_token_expire_minutes
    
    def create_access_token(self, user: User) -> Token:
        """Create a JWT access token for a user."""
        try:
            expires_delta = timedelta(minutes=self.access_token_expire_minutes)
            expire = datetime.utcnow() + expires_delta
            
            to_encode = {
                "sub": user.email,
                "user_id": user.user_id,
                "exp": expire
            }
            
            encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
            
            logger.debug(f"Created access token for user: {user.email}")
            return Token(
                access_token=encoded_jwt,
                token_type="bearer",
                expires_in=self.access_token_expire_minutes * 60
            )
            
        except Exception as e:
            logger.error(f"Error creating access token: {str(e)}")
            raise ValueError(f"Failed to create access token: {str(e)}")
    
    def verify_token(self, token: str) -> Optional[str]:
        """Verify and decode a JWT token, return user_id if valid."""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            user_id: Optional[str] = payload.get("user_id")
            
            if user_id is None:
                logger.warning("Token missing user_id")
                return None
            
            logger.debug(f"Token verified for user_id: {user_id}")
            return user_id
            
        except JWTError as e:
            logger.warning(f"JWT token verification failed: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"Error verifying token: {str(e)}")
            return None
    
    def get_token_expiration_time(self) -> int:
        """Get token expiration time in seconds."""
        return self.access_token_expire_minutes * 60 