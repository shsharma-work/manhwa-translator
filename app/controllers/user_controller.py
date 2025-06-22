"""
User controller for handling user-related HTTP requests.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from app.controllers.base import BaseController
from app.schemas.user import UserResponse
from app.services.user_service import UserService
from app.core.dependencies import get_user_service
from app.dependencies.auth import get_current_user

router = APIRouter(prefix="/users", tags=["users"])


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


@router.get("/{user_id}", response_model=UserResponse)
async def get_user_by_id(
    user_id: str,
    user_service: UserService = Depends(get_user_service),
    current_user = Depends(get_current_user)
):
    """
    Get user by ID.
    
    Returns the profile information of a specific user.
    Requires Bearer token authentication.
    """
    try:
        # For now, users can only access their own profile
        # In the future, this could be extended with admin roles
        if current_user.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied"
            )
        
        user = await user_service.get_user_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        return UserResponse(
            user_id=user.user_id,
            email=user.email,
            username=user.username,
            created_at=user.created_at,
            updated_at=user.updated_at,
            is_active=user.is_active,
            is_verified=user.is_verified
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise BaseController.handle_exception(e, "get user by ID") 