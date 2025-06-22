"""
Firestore database implementation.
"""
import firebase_admin
from firebase_admin import credentials, firestore
from typing import Any, Dict, List, Optional
import json
import os
from app.core.config import settings
from app.core.logging import get_logger
from app.database.base import DatabaseInterface, DatabaseError, DocumentNotFoundError, DuplicateDocumentError

logger = get_logger(__name__)


class FirestoreDB(DatabaseInterface):
    """Firestore database implementation."""
    
    def __init__(self):
        self.db: Optional[Any] = None
        self._initialize_firestore()
    
    def _initialize_firestore(self) -> None:
        """Initialize Firestore connection."""
        try:
            # Check if Firebase app is already initialized
            if not firebase_admin._apps:
                # Try to load from service account file first
                service_account_path = "firebase-service-account.json"
                
                if os.path.exists(service_account_path):
                    logger.info(f"Loading Firebase credentials from: {service_account_path}")
                    cred = credentials.Certificate(service_account_path)
                else:
                    # Fall back to environment variables
                    logger.info("Loading Firebase credentials from environment variables")
                    logger.debug(f"Project ID: {settings.database.firebase_project_id}")
                    
                    # Check if we have the minimum required credentials
                    if not settings.database.firebase_project_id:
                        raise ValueError("Firebase project ID is required")
                    
                    if not settings.database.firebase_private_key or not settings.database.firebase_client_email:
                        logger.warning("Firebase credentials not fully configured. Some features may not work.")
                        # Create a minimal credential for development
                        cred_dict = {
                            "type": "service_account",
                            "project_id": settings.database.firebase_project_id,
                            "auth_uri": settings.database.firebase_auth_uri,
                            "token_uri": settings.database.firebase_token_uri,
                            "auth_provider_x509_cert_url": settings.database.firebase_auth_provider_x509_cert_url,
                        }
                    else:
                        cred_dict = {
                            "type": "service_account",
                            "project_id": settings.database.firebase_project_id,
                            "private_key_id": settings.database.firebase_private_key_id,
                            "private_key": settings.database.firebase_private_key.replace("\\n", "\n") if settings.database.firebase_private_key else None,
                            "client_email": settings.database.firebase_client_email,
                            "client_id": settings.database.firebase_client_id,
                            "auth_uri": settings.database.firebase_auth_uri,
                            "token_uri": settings.database.firebase_token_uri,
                            "auth_provider_x509_cert_url": settings.database.firebase_auth_provider_x509_cert_url,
                            "client_x509_cert_url": settings.database.firebase_client_x509_cert_url
                        }
                    
                    # Remove None values
                    cred_dict = {k: v for k, v in cred_dict.items() if v is not None}
                    
                    cred = credentials.Certificate(cred_dict)
                
                firebase_admin.initialize_app(cred)
            
            self.db = firestore.client()
            logger.info(f"Firestore connection established successfully for project: {settings.database.firebase_project_id}")
            
        except Exception as e:
            logger.error(f"Error initializing Firestore: {str(e)}")
            logger.info("Make sure you have:")
            logger.info("  1. Created a Firebase project")
            logger.info("  2. Enabled Firestore Database")
            logger.info("  3. Downloaded service account key as 'firebase-service-account.json'")
            logger.info("  4. Or configured environment variables in .env file")
            raise DatabaseError(f"Failed to initialize Firestore: {str(e)}")
    
    async def create(self, collection: str, data: Dict[str, Any], document_id: Optional[str] = None) -> str:
        """Create a new document in Firestore."""
        try:
            if not self.db:
                raise DatabaseError("Firestore not initialized")
            
            collection_ref = self.db.collection(collection)
            
            if document_id:
                doc_ref = collection_ref.document(document_id)
                doc_ref.set(data)
                logger.debug(f"Created document {document_id} in collection {collection}")
                return document_id
            else:
                doc_ref = collection_ref.add(data)[1]
                logger.debug(f"Created document {doc_ref.id} in collection {collection}")
                return doc_ref.id
                
        except Exception as e:
            logger.error(f"Error creating document in collection {collection}: {str(e)}")
            raise DatabaseError(f"Failed to create document: {str(e)}")
    
    async def get(self, collection: str, document_id: str) -> Optional[Dict[str, Any]]:
        """Get a document by ID from Firestore."""
        try:
            if not self.db:
                raise DatabaseError("Firestore not initialized")
            
            doc_ref = self.db.collection(collection).document(document_id)
            doc = doc_ref.get()
            
            if doc.exists:
                data = doc.to_dict()
                data['id'] = doc.id
                logger.debug(f"Retrieved document {document_id} from collection {collection}")
                return data
            else:
                logger.debug(f"Document {document_id} not found in collection {collection}")
                return None
                
        except Exception as e:
            logger.error(f"Error getting document {document_id} from collection {collection}: {str(e)}")
            raise DatabaseError(f"Failed to get document: {str(e)}")
    
    async def update(self, collection: str, document_id: str, data: Dict[str, Any]) -> bool:
        """Update a document in Firestore."""
        try:
            if not self.db:
                raise DatabaseError("Firestore not initialized")
            
            doc_ref = self.db.collection(collection).document(document_id)
            doc_ref.update(data)
            logger.debug(f"Updated document {document_id} in collection {collection}")
            return True
            
        except Exception as e:
            logger.error(f"Error updating document {document_id} in collection {collection}: {str(e)}")
            raise DatabaseError(f"Failed to update document: {str(e)}")
    
    async def delete(self, collection: str, document_id: str) -> bool:
        """Delete a document from Firestore."""
        try:
            if not self.db:
                raise DatabaseError("Firestore not initialized")
            
            doc_ref = self.db.collection(collection).document(document_id)
            doc_ref.delete()
            logger.debug(f"Deleted document {document_id} from collection {collection}")
            return True
            
        except Exception as e:
            logger.error(f"Error deleting document {document_id} from collection {collection}: {str(e)}")
            raise DatabaseError(f"Failed to delete document: {str(e)}")
    
    async def list(self, collection: str, filters: Optional[Dict[str, Any]] = None, limit: int = 100) -> List[Dict[str, Any]]:
        """List documents from Firestore with optional filters."""
        try:
            if not self.db:
                raise DatabaseError("Firestore not initialized")
            
            collection_ref = self.db.collection(collection)
            query = collection_ref.limit(limit)
            
            # Apply filters if provided
            if filters:
                for field, value in filters.items():
                    query = query.where(field, "==", value)
            
            docs = query.stream()
            results = []
            
            for doc in docs:
                data = doc.to_dict()
                data['id'] = doc.id
                results.append(data)
            
            logger.debug(f"Retrieved {len(results)} documents from collection {collection}")
            return results
            
        except Exception as e:
            logger.error(f"Error listing documents from collection {collection}: {str(e)}")
            raise DatabaseError(f"Failed to list documents: {str(e)}")
    
    async def query(self, collection: str, field: str, operator: str, value: Any, limit: int = 100) -> List[Dict[str, Any]]:
        """Query documents by field in Firestore."""
        try:
            if not self.db:
                raise DatabaseError("Firestore not initialized")
            
            collection_ref = self.db.collection(collection)
            query = collection_ref.where(field, operator, value).limit(limit)
            docs = query.stream()
            
            results = []
            for doc in docs:
                data = doc.to_dict()
                data['id'] = doc.id
                results.append(data)
            
            logger.debug(f"Query returned {len(results)} documents from collection {collection}")
            return results
            
        except Exception as e:
            logger.error(f"Error querying documents from collection {collection}: {str(e)}")
            raise DatabaseError(f"Failed to query documents: {str(e)}")
    
    def get_collection(self, collection_name: str):
        """Get a Firestore collection reference (legacy method)."""
        if not self.db:
            raise DatabaseError("Firestore not initialized")
        return self.db.collection(collection_name)
    
    def get_document(self, collection_name: str, document_id: str):
        """Get a Firestore document reference (legacy method)."""
        if not self.db:
            raise DatabaseError("Firestore not initialized")
        return self.db.collection(collection_name).document(document_id)


# Global Firestore instance
firestore_db = FirestoreDB() 