from typing import Optional, List
from app.database.firestore import firestore_db
from app.models.user import User
from app.schemas.user import UserCreate
from app.services.auth import auth_service
import uuid


class UserService:
    def __init__(self):
        self.collection_name = "users"
    
    def create_user(self, user_data: UserCreate) -> User:
        """Create a new user in Firestore"""
        # Check if user already exists
        existing_user = self.get_user_by_email(user_data.email)
        if existing_user:
            raise ValueError("User with this email already exists")
        
        existing_username = self.get_user_by_username(user_data.username)
        if existing_username:
            raise ValueError("Username already taken")
        
        # Create new user
        user_id = str(uuid.uuid4())
        hashed_password = auth_service.get_password_hash(user_data.password)
        
        user = User(
            user_id=user_id,
            email=user_data.email,
            username=user_data.username,
            hashed_password=hashed_password
        )
        
        # Save to Firestore
        user_ref = firestore_db.get_document(self.collection_name, user_id)
        user_ref.set(user.to_dict())
        
        return user
    
    def get_user_by_id(self, user_id: str) -> Optional[User]:
        """Get user by ID from Firestore"""
        try:
            user_ref = firestore_db.get_document(self.collection_name, user_id)
            user_doc = user_ref.get()
            
            if user_doc.exists:
                return User.from_dict(user_doc.to_dict(), user_id)
            return None
        except Exception as e:
            print(f"Error getting user by ID: {e}")
            return None
    
    def get_user_by_email(self, email: str) -> Optional[User]:
        """Get user by email from Firestore"""
        try:
            users_ref = firestore_db.get_collection(self.collection_name)
            query = users_ref.where("email", "==", email).limit(1)
            docs = query.stream()
            
            for doc in docs:
                return User.from_dict(doc.to_dict(), doc.id)
            return None
        except Exception as e:
            print(f"Error getting user by email: {e}")
            return None
    
    def get_user_by_username(self, username: str) -> Optional[User]:
        """Get user by username from Firestore"""
        try:
            users_ref = firestore_db.get_collection(self.collection_name)
            query = users_ref.where("username", "==", username).limit(1)
            docs = query.stream()
            
            for doc in docs:
                return User.from_dict(doc.to_dict(), doc.id)
            return None
        except Exception as e:
            print(f"Error getting user by username: {e}")
            return None
    
    def authenticate_user(self, email: str, password: str) -> Optional[User]:
        """Authenticate user with email and password"""
        user = self.get_user_by_email(email)
        if not user:
            return None
        
        if not auth_service.verify_password(password, user.hashed_password):
            return None
        
        if not user.is_active:
            return None
        
        return user
    
    def get_all_users(self, limit: int = 100) -> List[User]:
        """Get all users (for admin purposes)"""
        try:
            users_ref = firestore_db.get_collection(self.collection_name)
            docs = users_ref.limit(limit).stream()
            
            users = []
            for doc in docs:
                users.append(User.from_dict(doc.to_dict(), doc.id))
            
            return users
        except Exception as e:
            print(f"Error getting all users: {e}")
            return []


# Global user service instance
user_service = UserService() 