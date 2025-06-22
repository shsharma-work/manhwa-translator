import firebase_admin
from firebase_admin import credentials, firestore
from app.config import settings
import json
import os
from typing import Optional


class FirestoreDB:
    def __init__(self):
        self.db: Optional[firestore.Client] = None
        self._initialize_firestore()
    
    def _initialize_firestore(self):
        """Initialize Firestore connection"""
        try:
            # Check if Firebase app is already initialized
            if not firebase_admin._apps:
                # Try to load from service account file first
                service_account_path = "firebase-service-account.json"
                
                if os.path.exists(service_account_path):
                    print(f"📁 Loading Firebase credentials from: {service_account_path}")
                    cred = credentials.Certificate(service_account_path)
                else:
                    # Fall back to environment variables
                    print(f"🔧 Loading Firebase credentials from environment variables")
                    print(f"📋 Project ID: {settings.firebase_project_id}")
                    
                    cred_dict = {
                        "type": "service_account",
                        "project_id": settings.firebase_project_id,
                        "private_key_id": settings.firebase_private_key_id,
                        "private_key": settings.firebase_private_key.replace("\\n", "\n") if settings.firebase_private_key else None,
                        "client_email": settings.firebase_client_email,
                        "client_id": settings.firebase_client_id,
                        "auth_uri": settings.firebase_auth_uri,
                        "token_uri": settings.firebase_token_uri,
                        "auth_provider_x509_cert_url": settings.firebase_auth_provider_x509_cert_url,
                        "client_x509_cert_url": settings.firebase_client_x509_cert_url
                    }
                    
                    # Remove None values
                    cred_dict = {k: v for k, v in cred_dict.items() if v is not None}
                    
                    if not cred_dict.get("project_id"):
                        raise ValueError("Firebase project ID is required")
                    
                    cred = credentials.Certificate(cred_dict)
                
                firebase_admin.initialize_app(cred)
            
            self.db = firestore.client()
            print(f"✅ Firestore connection established successfully for project: {settings.firebase_project_id}")
            
        except Exception as e:
            print(f"❌ Error initializing Firestore: {str(e)}")
            print(f"💡 Make sure you have:")
            print(f"   1. Created a Firebase project named 'manhwa-translator'")
            print(f"   2. Enabled Firestore Database")
            print(f"   3. Downloaded service account key as 'firebase-service-account.json'")
            print(f"   4. Or configured environment variables in .env file")
            raise
    
    def get_collection(self, collection_name: str):
        """Get a Firestore collection reference"""
        if not self.db:
            raise RuntimeError("Firestore not initialized")
        return self.db.collection(collection_name)
    
    def get_document(self, collection_name: str, document_id: str):
        """Get a Firestore document reference"""
        if not self.db:
            raise RuntimeError("Firestore not initialized")
        return self.db.collection(collection_name).document(document_id)


# Global Firestore instance
firestore_db = FirestoreDB() 