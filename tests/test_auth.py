import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.services.user import user_service
from app.services.auth import auth_service

client = TestClient(app)


class TestAuth:
    def test_register_user_success(self):
        """Test successful user registration"""
        user_data = {
            "email": "test@example.com",
            "username": "testuser",
            "password": "TestPass123"
        }
        
        response = client.post("/auth/register", json=user_data)
        assert response.status_code == 201
        
        data = response.json()
        assert data["email"] == user_data["email"]
        assert data["username"] == user_data["username"]
        assert "user_id" in data
        assert "created_at" in data
        assert "updated_at" in data
        assert data["is_active"] is True
        assert data["is_verified"] is False
    
    def test_register_user_duplicate_email(self):
        """Test registration with duplicate email"""
        user_data = {
            "email": "duplicate@example.com",
            "username": "user1",
            "password": "TestPass123"
        }
        
        # Register first user
        response = client.post("/auth/register", json=user_data)
        assert response.status_code == 201
        
        # Try to register with same email
        user_data["username"] = "user2"
        response = client.post("/auth/register", json=user_data)
        assert response.status_code == 400
        assert "email already exists" in response.json()["detail"]
    
    def test_register_user_duplicate_username(self):
        """Test registration with duplicate username"""
        user_data = {
            "email": "user1@example.com",
            "username": "duplicateuser",
            "password": "TestPass123"
        }
        
        # Register first user
        response = client.post("/auth/register", json=user_data)
        assert response.status_code == 201
        
        # Try to register with same username
        user_data["email"] = "user2@example.com"
        response = client.post("/auth/register", json=user_data)
        assert response.status_code == 400
        assert "Username already taken" in response.json()["detail"]
    
    def test_register_user_weak_password(self):
        """Test registration with weak password"""
        user_data = {
            "email": "test@example.com",
            "username": "testuser",
            "password": "weak"
        }
        
        response = client.post("/auth/register", json=user_data)
        assert response.status_code == 422  # Validation error
    
    def test_register_user_invalid_email(self):
        """Test registration with invalid email"""
        user_data = {
            "email": "invalid-email",
            "username": "testuser",
            "password": "TestPass123"
        }
        
        response = client.post("/auth/register", json=user_data)
        assert response.status_code == 422  # Validation error
    
    def test_register_user_invalid_username(self):
        """Test registration with invalid username"""
        user_data = {
            "email": "test@example.com",
            "username": "test user",  # Contains space
            "password": "TestPass123"
        }
        
        response = client.post("/auth/register", json=user_data)
        assert response.status_code == 422  # Validation error
    
    def test_login_user_success(self):
        """Test successful user login"""
        # First register a user
        user_data = {
            "email": "login@example.com",
            "username": "loginuser",
            "password": "TestPass123"
        }
        
        register_response = client.post("/auth/register", json=user_data)
        assert register_response.status_code == 201
        
        # Then login
        login_data = {
            "email": user_data["email"],
            "password": user_data["password"]
        }
        
        response = client.post("/auth/login", json=login_data)
        assert response.status_code == 200
        
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
        assert "expires_in" in data
    
    def test_login_user_invalid_credentials(self):
        """Test login with invalid credentials"""
        login_data = {
            "email": "nonexistent@example.com",
            "password": "wrongpassword"
        }
        
        response = client.post("/auth/login", json=login_data)
        assert response.status_code == 401
        assert "Incorrect email or password" in response.json()["detail"]
    
    def test_login_user_wrong_password(self):
        """Test login with wrong password"""
        # First register a user
        user_data = {
            "email": "wrongpass@example.com",
            "username": "wrongpassuser",
            "password": "TestPass123"
        }
        
        register_response = client.post("/auth/register", json=user_data)
        assert register_response.status_code == 201
        
        # Then login with wrong password
        login_data = {
            "email": user_data["email"],
            "password": "WrongPassword123"
        }
        
        response = client.post("/auth/login", json=login_data)
        assert response.status_code == 401
        assert "Incorrect email or password" in response.json()["detail"] 