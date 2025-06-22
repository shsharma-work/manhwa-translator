import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


class TestUsers:
    def test_get_current_user_profile_success(self):
        """Test getting current user profile with valid token"""
        # First register and login to get token
        user_data = {
            "email": "profile@example.com",
            "username": "profileuser",
            "password": "TestPass123"
        }
        
        # Register user
        register_response = client.post("/auth/register", json=user_data)
        assert register_response.status_code == 201
        
        # Login to get token
        login_response = client.post("/auth/login", json={
            "email": user_data["email"],
            "password": user_data["password"]
        })
        assert login_response.status_code == 200
        
        token = login_response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        
        # Get profile
        response = client.get("/users/me", headers=headers)
        assert response.status_code == 200
        
        data = response.json()
        assert data["email"] == user_data["email"]
        assert data["username"] == user_data["username"]
        assert "user_id" in data
        assert "created_at" in data
        assert "updated_at" in data
    
    def test_get_current_user_profile_no_token(self):
        """Test getting current user profile without token"""
        response = client.get("/users/me")
        assert response.status_code == 403  # Forbidden
    
    def test_get_current_user_profile_invalid_token(self):
        """Test getting current user profile with invalid token"""
        headers = {"Authorization": "Bearer invalid_token"}
        response = client.get("/users/me", headers=headers)
        assert response.status_code == 401  # Unauthorized 