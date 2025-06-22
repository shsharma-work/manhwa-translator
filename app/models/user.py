from datetime import datetime
from typing import Optional, Dict, Any


class User:
    def __init__(
        self,
        email: str,
        username: str,
        hashed_password: str,
        user_id: str,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
        is_active: bool = True,
        is_verified: bool = False
    ):
        self.user_id = user_id
        self.email = email
        self.username = username
        self.hashed_password = hashed_password
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()
        self.is_active = is_active
        self.is_verified = is_verified
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert user to dictionary for Firestore storage"""
        return {
            "email": self.email,
            "username": self.username,
            "hashed_password": self.hashed_password,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "is_active": self.is_active,
            "is_verified": self.is_verified
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any], user_id: str) -> "User":
        """Create user from Firestore document data"""
        # Handle datetime conversion from Firestore timestamp
        created_at = data.get("created_at")
        if created_at is not None:
            if hasattr(created_at, 'timestamp'):
                created_at = datetime.fromtimestamp(created_at.timestamp())
            elif isinstance(created_at, (int, float)):
                created_at = datetime.fromtimestamp(created_at)
            else:
                created_at = datetime.utcnow()
        else:
            created_at = datetime.utcnow()
        
        updated_at = data.get("updated_at")
        if updated_at is not None:
            if hasattr(updated_at, 'timestamp'):
                updated_at = datetime.fromtimestamp(updated_at.timestamp())
            elif isinstance(updated_at, (int, float)):
                updated_at = datetime.fromtimestamp(updated_at)
            else:
                updated_at = datetime.utcnow()
        else:
            updated_at = datetime.utcnow()
        
        return cls(
            user_id=user_id,
            email=data.get("email", ""),
            username=data.get("username", ""),
            hashed_password=data.get("hashed_password", ""),
            created_at=created_at,
            updated_at=updated_at,
            is_active=data.get("is_active", True),
            is_verified=data.get("is_verified", False)
        )
    
    def update_timestamp(self):
        """Update the updated_at timestamp"""
        self.updated_at = datetime.utcnow() 