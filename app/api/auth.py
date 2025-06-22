from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.schemas.user import UserCreate, UserLogin, UserResponse, Token
from app.services.user import user_service
from app.services.auth import auth_service
from datetime import timedelta
import traceback

router = APIRouter(prefix="/auth", tags=["authentication"])
security = HTTPBearer()


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register_user(user_data: UserCreate):
    """
    Register a new user
    
    - **email**: User's email address (must be unique)
    - **username**: User's username (must be unique, 3-50 characters, alphanumeric + underscore)
    - **password**: User's password (min 8 chars, must contain uppercase, lowercase, and digit)
    """
    try:
        print(f"🔍 Attempting to register user: {user_data.email}")
        user = user_service.create_user(user_data)
        print(f"✅ User created successfully: {user.user_id}")
        
        return UserResponse(
            user_id=user.user_id,
            email=user.email,
            username=user.username,
            created_at=user.created_at,
            updated_at=user.updated_at,
            is_active=user.is_active,
            is_verified=user.is_verified
        )
    except ValueError as e:
        print(f"❌ Validation error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        print(f"❌ Internal server error: {str(e)}")
        print(f"📋 Full traceback: {traceback.format_exc()}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )


@router.post("/login", response_model=Token)
def login_user(user_credentials: UserLogin):
    """
    Login user and get access token
    
    - **email**: User's email address
    - **password**: User's password
    """
    try:
        user = user_service.authenticate_user(
            user_credentials.email, 
            user_credentials.password
        )
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Create access token
        access_token_expires = timedelta(minutes=auth_service.get_token_expiration_time() / 60)
        access_token = auth_service.create_access_token(
            data={"sub": user.email, "user_id": user.user_id},
            expires_delta=access_token_expires
        )
        
        return Token(
            access_token=access_token,
            token_type="bearer",
            expires_in=auth_service.get_token_expiration_time()
        )
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Login error: {str(e)}")
        print(f"📋 Full traceback: {traceback.format_exc()}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    Get current authenticated user from JWT token
    """
    token = credentials.credentials
    token_data = auth_service.verify_token(token)
    
    if token_data is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Ensure user_id is not None
    if token_data.user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token format",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user = user_service.get_user_by_id(token_data.user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    
    return user 