"""
Authentication controller for handling auth-related HTTP requests.
"""
from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from app.controllers.base import BaseController
from app.schemas.user import UserCreate, UserLogin, UserResponse, Token
from app.services.auth_service import AuthService
from app.services.user_service import UserService
from app.core.dependencies import get_auth_service, get_user_service
from app.dependencies.auth import get_current_user

router = APIRouter(prefix="/auth", tags=["authentication"])


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register_user(
    user_data: UserCreate,
    auth_service: AuthService = Depends(get_auth_service),
    user_service: UserService = Depends(get_user_service)
):
    """
    Register a new user.
    
    - **email**: User's email address (must be unique)
    - **username**: User's username (must be unique, 3-50 characters, alphanumeric + underscore)
    - **password**: User's password (min 8 chars, must contain uppercase, lowercase, and digit)
    """
    try:
        user = await auth_service.register_user(user_data)
        return UserResponse(
            user_id=user.user_id,
            email=user.email,
            username=user.username,
            created_at=user.created_at,
            updated_at=user.updated_at,
            is_active=user.is_active,
            is_verified=user.is_verified
        )
    except Exception as e:
        raise BaseController.handle_exception(e, "user registration")


@router.post("/login", response_model=Token)
async def login_user(
    user_credentials: UserLogin,
    auth_service: AuthService = Depends(get_auth_service)
):
    """
    Login user and get access token.
    
    - **email**: User's email address
    - **password**: User's password
    """
    try:
        token_data = await auth_service.login_user(user_credentials)
        return token_data
    except Exception as e:
        raise BaseController.handle_exception(e, "user login")


@router.get("/me", response_model=UserResponse)
async def get_current_user_profile(
    current_user = Depends(get_current_user)
):
    """
    Get current user profile.
    
    Returns the profile information of the currently authenticated user.
    Requires Bearer token authentication.
    """
    try:
        return UserResponse(
            user_id=current_user.user_id,
            email=current_user.email,
            username=current_user.username,
            created_at=current_user.created_at,
            updated_at=current_user.updated_at,
            is_active=current_user.is_active,
            is_verified=current_user.is_verified
        )
    except Exception as e:
        raise BaseController.handle_exception(e, "get user profile") 