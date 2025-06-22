"""
Authentication service for handling authentication business logic.
"""
from datetime import timedelta
from typing import Optional
from app.core.logging import get_logger
from app.core.exceptions import AuthenticationError, ValidationError, ConflictError
from app.schemas.user import UserCreate, UserLogin, Token
from app.models.user import User
from app.services.user_service import UserService
from app.services.jwt_service import JWTService

logger = get_logger(__name__)


class AuthService:
    """Authentication service for user registration and login."""
    
    def __init__(self, user_service: UserService, jwt_service: JWTService):
        self.user_service = user_service
        self.jwt_service = jwt_service
    
    async def register_user(self, user_data: UserCreate) -> User:
        """Register a new user."""
        try:
            # Validate input data
            self._validate_user_data(user_data)
            
            # Create user
            user = await self.user_service.create_user(user_data)
            
            logger.info(f"User registered successfully: {user.email}")
            return user
            
        except (ValidationError, ConflictError):
            raise
        except Exception as e:
            logger.error(f"Registration failed: {str(e)}")
            raise AuthenticationError(f"Registration failed: {str(e)}")
    
    async def login_user(self, credentials: UserLogin) -> Token:
        """Login user and return access token."""
        try:
            # Authenticate user
            user = await self.user_service.authenticate_user(
                credentials.email, 
                credentials.password
            )
            
            if not user:
                raise AuthenticationError("Invalid email or password")
            
            # Generate access token
            token_data = self.jwt_service.create_access_token(user)
            
            logger.info(f"User logged in successfully: {user.email}")
            return token_data
            
        except AuthenticationError:
            raise
        except Exception as e:
            logger.error(f"Login failed: {str(e)}")
            raise AuthenticationError(f"Login failed: {str(e)}")
    
    async def verify_token(self, token: str) -> Optional[User]:
        """Verify JWT token and return user."""
        try:
            user_id = self.jwt_service.verify_token(token)
            if not user_id:
                return None
            
            user = await self.user_service.get_user_by_id(user_id)
            if not user or not user.is_active:
                return None
            
            return user
            
        except Exception as e:
            logger.error(f"Token verification failed: {str(e)}")
            return None
    
    def _validate_user_data(self, user_data: UserCreate) -> None:
        """Validate user registration data."""
        # Email validation
        if not user_data.email or '@' not in user_data.email:
            raise ValidationError("Invalid email format")
        
        # Username validation
        if not user_data.username or len(user_data.username) < 3:
            raise ValidationError("Username must be at least 3 characters long")
        
        # Password validation
        if not user_data.password or len(user_data.password) < 8:
            raise ValidationError("Password must be at least 8 characters long") 