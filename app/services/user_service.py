"""
User service for managing user operations.
"""
from typing import Optional, List
import uuid
from app.core.logging import get_logger
from app.core.exceptions import ValidationError, ConflictError, NotFoundError, DatabaseError, AuthenticationError
from app.database.firestore import FirestoreDB
from app.models.user import User
from app.schemas.user import UserCreate
from app.services.password_service import PasswordService

logger = get_logger(__name__)


class UserService:
    """User service for managing user operations."""
    
    def __init__(self, firestore_db: FirestoreDB, password_service: PasswordService):
        self.collection_name = "users"
        self.firestore_db = firestore_db
        self.password_service = password_service
    
    async def create_user(self, user_data: UserCreate) -> User:
        """Create a new user in Firestore."""
        try:
            # Check if user already exists
            existing_user = await self.get_user_by_email(user_data.email)
            if existing_user:
                raise ConflictError("User with this email already exists")
            
            existing_username = await self.get_user_by_username(user_data.username)
            if existing_username:
                raise ConflictError("Username already taken")
            
            # Create new user
            user_id = str(uuid.uuid4())
            hashed_password = self.password_service.hash_password(user_data.password)
            
            user = User(
                user_id=user_id,
                email=user_data.email,
                username=user_data.username,
                hashed_password=hashed_password
            )
            
            # Save to Firestore
            await self.firestore_db.create(self.collection_name, user.to_dict(), user_id)
            
            logger.info(f"Created new user: {user.email} with ID: {user.user_id}")
            return user
            
        except (ConflictError, ValidationError):
            raise
        except Exception as e:
            logger.error(f"Error creating user: {str(e)}")
            raise DatabaseError(f"Failed to create user: {str(e)}")
    
    async def get_user_by_id(self, user_id: str) -> Optional[User]:
        """Get user by ID from Firestore."""
        try:
            user_data = await self.firestore_db.get(self.collection_name, user_id)
            
            if user_data:
                user = User.from_dict(user_data, user_id)
                logger.debug(f"Retrieved user by ID: {user_id}")
                return user
            return None
            
        except Exception as e:
            logger.error(f"Error getting user by ID {user_id}: {str(e)}")
            raise DatabaseError(f"Failed to get user: {str(e)}")
    
    async def get_user_by_email(self, email: str) -> Optional[User]:
        """Get user by email from Firestore."""
        try:
            users_data = await self.firestore_db.query(self.collection_name, "email", "==", email, limit=1)
            
            if users_data:
                user_data = users_data[0]
                user = User.from_dict(user_data, user_data['id'])
                logger.debug(f"Retrieved user by email: {email}")
                return user
            return None
            
        except Exception as e:
            logger.error(f"Error getting user by email {email}: {str(e)}")
            raise DatabaseError(f"Failed to get user: {str(e)}")
    
    async def get_user_by_username(self, username: str) -> Optional[User]:
        """Get user by username from Firestore."""
        try:
            users_data = await self.firestore_db.query(self.collection_name, "username", "==", username, limit=1)
            
            if users_data:
                user_data = users_data[0]
                user = User.from_dict(user_data, user_data['id'])
                logger.debug(f"Retrieved user by username: {username}")
                return user
            return None
            
        except Exception as e:
            logger.error(f"Error getting user by username {username}: {str(e)}")
            raise DatabaseError(f"Failed to get user: {str(e)}")
    
    async def authenticate_user(self, email: str, password: str) -> Optional[User]:
        """Authenticate user with email and password."""
        try:
            user = await self.get_user_by_email(email)
            if not user:
                logger.warning(f"Authentication failed: user not found for email {email}")
                return None
            
            if not self.password_service.verify_password(password, user.hashed_password):
                logger.warning(f"Authentication failed: invalid password for email {email}")
                return None
            
            if not user.is_active:
                logger.warning(f"Authentication failed: inactive user {email}")
                return None
            
            logger.info(f"User authenticated successfully: {email}")
            return user
            
        except Exception as e:
            logger.error(f"Error authenticating user {email}: {str(e)}")
            raise DatabaseError(f"Failed to authenticate user: {str(e)}")
    
    async def get_all_users(self, limit: int = 100) -> List[User]:
        """Get all users (for admin purposes)."""
        try:
            users_data = await self.firestore_db.list(self.collection_name, limit=limit)
            
            users = []
            for user_data in users_data:
                user = User.from_dict(user_data, user_data['id'])
                users.append(user)
            
            logger.debug(f"Retrieved {len(users)} users")
            return users
            
        except Exception as e:
            logger.error(f"Error getting all users: {str(e)}")
            raise DatabaseError(f"Failed to get users: {str(e)}")
    
    async def update_user(self, user_id: str, update_data: dict) -> User:
        """Update user information."""
        try:
            user = await self.get_user_by_id(user_id)
            if not user:
                raise NotFoundError(f"User with ID {user_id} not found")
            
            # Update user data
            for key, value in update_data.items():
                if hasattr(user, key):
                    setattr(user, key, value)
            
            user.update_timestamp()
            
            # Save to database
            await self.firestore_db.update(self.collection_name, user_id, user.to_dict())
            
            logger.info(f"Updated user: {user_id}")
            return user
            
        except (NotFoundError, ValidationError):
            raise
        except Exception as e:
            logger.error(f"Error updating user {user_id}: {str(e)}")
            raise DatabaseError(f"Failed to update user: {str(e)}")
    
    async def delete_user(self, user_id: str) -> bool:
        """Delete a user."""
        try:
            user = await self.get_user_by_id(user_id)
            if not user:
                raise NotFoundError(f"User with ID {user_id} not found")
            
            await self.firestore_db.delete(self.collection_name, user_id)
            
            logger.info(f"Deleted user: {user_id}")
            return True
            
        except NotFoundError:
            raise
        except Exception as e:
            logger.error(f"Error deleting user {user_id}: {str(e)}")
            raise DatabaseError(f"Failed to delete user: {str(e)}") 