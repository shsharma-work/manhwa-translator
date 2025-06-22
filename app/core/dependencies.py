"""
Dependency injection system for the Manhwa Translator API.
"""
from typing import Generator
from fastapi import Depends
from app.core.config import settings
from app.core.logging import get_logger
from app.database.firestore import FirestoreDB
from app.services.auth_service import AuthService
from app.services.user_service import UserService
from app.services.jwt_service import JWTService
from app.services.password_service import PasswordService

logger = get_logger(__name__)


class ServiceContainer:
    """Service container for dependency injection."""
    
    def __init__(self):
        self._firestore_db: FirestoreDB | None = None
        self._password_service: PasswordService | None = None
        self._jwt_service: JWTService | None = None
        self._user_service: UserService | None = None
        self._auth_service: AuthService | None = None
    
    @property
    def firestore_db(self) -> FirestoreDB:
        """Get Firestore database instance."""
        if self._firestore_db is None:
            logger.info("Initializing Firestore database connection")
            self._firestore_db = FirestoreDB()
        return self._firestore_db
    
    @property
    def password_service(self) -> PasswordService:
        """Get password service instance."""
        if self._password_service is None:
            logger.info("Initializing password service")
            self._password_service = PasswordService()
        return self._password_service
    
    @property
    def jwt_service(self) -> JWTService:
        """Get JWT service instance."""
        if self._jwt_service is None:
            logger.info("Initializing JWT service")
            self._jwt_service = JWTService()
        return self._jwt_service
    
    @property
    def user_service(self) -> UserService:
        """Get user service instance."""
        if self._user_service is None:
            logger.info("Initializing user service")
            self._user_service = UserService(self.firestore_db, self.password_service)
        return self._user_service
    
    @property
    def auth_service(self) -> AuthService:
        """Get authentication service instance."""
        if self._auth_service is None:
            logger.info("Initializing authentication service")
            self._auth_service = AuthService(self.user_service, self.jwt_service)
        return self._auth_service


# Global service container
service_container = ServiceContainer()


def get_firestore_db() -> FirestoreDB:
    """Dependency to get Firestore database instance."""
    return service_container.firestore_db


def get_password_service() -> PasswordService:
    """Dependency to get password service instance."""
    return service_container.password_service


def get_jwt_service() -> JWTService:
    """Dependency to get JWT service instance."""
    return service_container.jwt_service


def get_user_service() -> UserService:
    """Dependency to get user service instance."""
    return service_container.user_service


def get_auth_service() -> AuthService:
    """Dependency to get authentication service instance."""
    return service_container.auth_service


def get_settings_dependency():
    """Dependency to get application settings."""
    return settings 