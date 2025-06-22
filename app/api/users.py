from fastapi import APIRouter, Depends
from app.schemas.user import UserResponse
from app.models.user import User
from app.api.auth import get_current_user

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=UserResponse)
def get_current_user_profile(current_user: User = Depends(get_current_user)):
    """
    Get current user profile
    
    Returns the profile information of the currently authenticated user.
    Requires Bearer token authentication.
    """
    return UserResponse(
        user_id=current_user.user_id,
        email=current_user.email,
        username=current_user.username,
        created_at=current_user.created_at,
        updated_at=current_user.updated_at,
        is_active=current_user.is_active,
        is_verified=current_user.is_verified
    ) 