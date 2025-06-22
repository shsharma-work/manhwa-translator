"""
Configuration management for the Manhwa Translator API.
"""
from pydantic_settings import BaseSettings
from typing import Optional, List
from functools import lru_cache


class DatabaseSettings(BaseSettings):
    """Database configuration settings."""
    firebase_project_id: str = "manhwa-translator-422ed"
    firebase_private_key_id: Optional[str] = None
    firebase_private_key: Optional[str] = None
    firebase_client_email: Optional[str] = None
    firebase_client_id: Optional[str] = None
    firebase_auth_uri: str = "https://accounts.google.com/o/oauth2/auth"
    firebase_token_uri: str = "https://oauth2.googleapis.com/token"
    firebase_auth_provider_x509_cert_url: str = "https://www.googleapis.com/oauth2/v1/certs"
    firebase_client_x509_cert_url: Optional[str] = None
    
    class Config:
        env_prefix = "FIREBASE_"


class SecuritySettings(BaseSettings):
    """Security configuration settings."""
    secret_key: str = "your-super-secret-key-change-this-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    password_min_length: int = 8
    password_max_length: int = 100
    
    class Config:
        env_prefix = ""


class ServerSettings(BaseSettings):
    """Server configuration settings."""
    debug: bool = True
    host: str = "0.0.0.0"
    port: int = 8000
    cors_origins: List[str] = ["*"]
    cors_allow_credentials: bool = True
    cors_allow_methods: List[str] = ["*"]
    cors_allow_headers: List[str] = ["*"]
    
    class Config:
        env_prefix = ""


class Settings(BaseSettings):
    """Main application settings."""
    # Application metadata
    app_name: str = "Manhwa Translator API"
    app_version: str = "1.0.0"
    app_description: str = "A professional FastAPI application for user authentication with Firestore database integration"
    
    # Sub-settings
    database: DatabaseSettings = DatabaseSettings()
    security: SecuritySettings = SecuritySettings()
    server: ServerSettings = ServerSettings()
    
    class Config:
        env_file = ".env"
        case_sensitive = False
        env_nested_delimiter = "__"
        # Allow extra fields for backward compatibility
        extra = "ignore"


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()


# Global settings instance
settings = get_settings() 