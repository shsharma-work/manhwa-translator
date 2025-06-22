"""
Base database interface for the Manhwa Translator API.
"""
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Generic, TypeVar
from app.core.logging import get_logger

logger = get_logger(__name__)

T = TypeVar('T')


class DatabaseInterface(ABC, Generic[T]):
    """Abstract base class for database operations."""
    
    @abstractmethod
    async def create(self, collection: str, data: Dict[str, Any], document_id: Optional[str] = None) -> str:
        """Create a new document."""
        pass
    
    @abstractmethod
    async def get(self, collection: str, document_id: str) -> Optional[Dict[str, Any]]:
        """Get a document by ID."""
        pass
    
    @abstractmethod
    async def update(self, collection: str, document_id: str, data: Dict[str, Any]) -> bool:
        """Update a document."""
        pass
    
    @abstractmethod
    async def delete(self, collection: str, document_id: str) -> bool:
        """Delete a document."""
        pass
    
    @abstractmethod
    async def list(self, collection: str, filters: Optional[Dict[str, Any]] = None, limit: int = 100) -> List[Dict[str, Any]]:
        """List documents with optional filters."""
        pass
    
    @abstractmethod
    async def query(self, collection: str, field: str, operator: str, value: Any, limit: int = 100) -> List[Dict[str, Any]]:
        """Query documents by field."""
        pass


class DatabaseError(Exception):
    """Base exception for database operations."""
    pass


class DocumentNotFoundError(DatabaseError):
    """Raised when a document is not found."""
    pass


class DuplicateDocumentError(DatabaseError):
    """Raised when trying to create a duplicate document."""
    pass 