"""
Authentication service for the Manhwa Translator API.
"""
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from app.core.config import settings
from app.core.logging import get_logger
from app.schemas.user import TokenData

logger = get_logger(__name__)


class AuthService:
    """Authentication service for JWT tokens and password hashing."""
    
    def __init__(self):
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self.secret_key = settings.security.secret_key
        self.algorithm = settings.security.algorithm
        self.access_token_expire_minutes = settings.security.access_token_expire_minutes
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify a password against its hash."""
        try:
            return self.pwd_context.verify(plain_password, hashed_password)
        except Exception as e:
            logger.error(f"Error verifying password: {str(e)}")
            return False
    
    def get_password_hash(self, password: str) -> str:
        """Hash a password using bcrypt."""
        try:
            return self.pwd_context.hash(password)
        except Exception as e:
            logger.error(f"Error hashing password: {str(e)}")
            raise ValueError(f"Failed to hash password: {str(e)}")
    
    def create_access_token(self, data: dict, expires_delta: Optional[timedelta] = None) -> str:
        """Create a JWT access token."""
        try:
            to_encode = data.copy()
            
            if expires_delta:
                expire = datetime.utcnow() + expires_delta
            else:
                expire = datetime.utcnow() + timedelta(minutes=self.access_token_expire_minutes)
            
            to_encode.update({"exp": expire})
            encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
            
            logger.debug(f"Created access token for user: {data.get('sub', 'unknown')}")
            return encoded_jwt
            
        except Exception as e:
            logger.error(f"Error creating access token: {str(e)}")
            raise ValueError(f"Failed to create access token: {str(e)}")
    
    def verify_token(self, token: str) -> Optional[TokenData]:
        """Verify and decode a JWT token."""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            email: Optional[str] = payload.get("sub")
            user_id: Optional[str] = payload.get("user_id")
            
            if email is None or user_id is None:
                logger.warning("Token missing required fields (sub or user_id)")
                return None
            
            token_data = TokenData(email=email, user_id=user_id)
            logger.debug(f"Token verified for user: {email}")
            return token_data
            
        except JWTError as e:
            logger.warning(f"JWT token verification failed: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"Error verifying token: {str(e)}")
            return None
    
    def get_token_expiration_time(self) -> int:
        """Get token expiration time in seconds."""
        return self.access_token_expire_minutes * 60


# Global auth service instance
auth_service = AuthService() 