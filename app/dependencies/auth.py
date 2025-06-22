"""
Authentication dependencies and utilities.
"""
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.core.logging import get_logger
from app.services.auth_service import AuthService
from app.core.dependencies import get_auth_service

logger = get_logger(__name__)

security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    auth_service: AuthService = Depends(get_auth_service)
):
    """Get current authenticated user from JWT token."""
    try:
        token = credentials.credentials
        user = await auth_service.verify_token(token)
        
        if user is None:
            logger.warning("Invalid token provided")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        return user
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting current user: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        ) 