# Manhwa Translator API

A professional FastAPI application for user authentication with Firestore database integration, built with a modular and scalable architecture.

## 🚀 Features

- **Modular Architecture**: Clean separation of concerns with well-organized modules
- **User Authentication**: JWT-based authentication with secure password hashing
- **Firestore Integration**: NoSQL database with real-time capabilities
- **Comprehensive Logging**: Structured logging throughout the application
- **Error Handling**: Custom exception handling with proper HTTP status codes
- **Input Validation**: Robust validation using Pydantic schemas
- **Security**: CORS middleware, input sanitization, and secure token generation
- **API Documentation**: Auto-generated OpenAPI documentation
- **Health Checks**: Built-in health monitoring endpoints
- **Dependency Injection**: Clean dependency management and service injection

## 📁 Project Structure

```
manhwa-translator/
├── app/
│   ├── controllers/           # HTTP request handlers
│   │   ├── __init__.py
│   │   ├── base.py           # Base controller with common functionality
│   │   ├── auth_controller.py # Authentication endpoints
│   │   └── user_controller.py # User management endpoints
│   ├── core/                  # Core application functionality
│   │   ├── __init__.py
│   │   ├── config.py          # Configuration management
│   │   ├── dependencies.py    # Dependency injection
│   │   ├── exceptions.py      # Custom exceptions
│   │   ├── logging.py         # Logging configuration
│   │   └── security.py        # Security utilities
│   ├── database/              # Database layer
│   │   ├── __init__.py
│   │   ├── base.py            # Database interface
│   │   └── firestore.py       # Firestore implementation
│   ├── dependencies/          # FastAPI dependencies
│   │   ├── __init__.py
│   │   └── auth.py            # Authentication dependencies
│   ├── middleware/            # Middleware components
│   │   ├── __init__.py
│   │   ├── cors.py            # CORS configuration
│   │   └── logging.py         # Request/response logging
│   ├── models/                # Data models
│   │   ├── __init__.py
│   │   └── user.py            # User model
│   ├── schemas/               # Pydantic schemas
│   │   ├── __init__.py
│   │   └── user.py            # User schemas
│   ├── services/              # Business logic layer
│   │   ├── __init__.py
│   │   ├── auth_service.py    # Authentication business logic
│   │   ├── jwt_service.py     # JWT token management
│   │   ├── password_service.py # Password hashing utilities
│   │   └── user_service.py    # User management business logic
│   ├── utils/                 # Utility functions
│   │   ├── __init__.py
│   │   └── validators.py      # Input validation utilities
│   ├── __init__.py
│   └── main.py                # Main application
├── tests/                     # Test suite
│   ├── __init__.py
│   ├── test_auth.py
│   └── test_users.py
├── .env.example               # Environment variables template
├── docker-compose.yml         # Docker Compose configuration
├── Dockerfile                 # Docker configuration
├── firebase-service-account.json  # Firebase credentials
├── pytest.ini                # Pytest configuration
├── README.md                  # This file
├── requirements.txt           # Python dependencies
├── run.py                     # Application runner
└── setup_firebase.py          # Firebase setup script
```

## 🛠️ Installation

### Prerequisites

- Python 3.8+
- Firebase project with Firestore enabled
- Firebase service account key

### Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd manhwa-translator
   ```

2. **Create virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Setup Firebase**
   ```bash
   python setup_firebase.py
   ```

## ⚙️ Configuration

The application uses a hierarchical configuration system:

### Environment Variables

```bash
# Application
APP_NAME="Manhwa Translator API"
APP_VERSION="1.0.0"
DEBUG=true

# Server
HOST="0.0.0.0"
PORT=8000

# Security
SECRET_KEY="your-super-secret-key"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Database
FIREBASE_PROJECT_ID="your-project-id"
FIREBASE_PRIVATE_KEY_ID="your-private-key-id"
FIREBASE_PRIVATE_KEY="your-private-key"
FIREBASE_CLIENT_EMAIL="your-client-email"
FIREBASE_CLIENT_ID="your-client-id"
FIREBASE_CLIENT_X509_CERT_URL="your-cert-url"

# CORS
CORS_ORIGINS=["*"]
CORS_ALLOW_CREDENTIALS=true
CORS_ALLOW_METHODS=["*"]
CORS_ALLOW_HEADERS=["*"]
```

## 🚀 Running the Application

### Development Mode
```bash
python run.py
```

### Production Mode
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### Using Docker
```bash
# Build and run with Docker Compose
docker-compose up --build

# Or build and run manually
docker build -t manhwa-translator .
docker run -p 8000:8000 manhwa-translator
```

## 📚 API Documentation

Once the application is running, you can access:

- **Interactive API Docs**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc
- **OpenAPI Schema**: http://localhost:8000/openapi.json

## 🔐 API Endpoints

### Authentication Endpoints

#### Register User
```http
POST /auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "username": "username",
  "password": "SecurePass123"
}
```

#### Login User
```http
POST /auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "SecurePass123"
}
```

#### Get Current User Profile
```http
GET /auth/me
Authorization: Bearer <your-jwt-token>
```

### User Management Endpoints

#### Get Current User Profile
```http
GET /users/me
Authorization: Bearer <your-jwt-token>
```

#### Get User by ID
```http
GET /users/{user_id}
Authorization: Bearer <your-jwt-token>
```

### Health Check Endpoints

#### API Information
```http
GET /
```

#### Health Status
```http
GET /health
```

## 🔐 Authentication

The API uses JWT-based authentication:

1. **Register a user** using `POST /auth/register`
2. **Login** using `POST /auth/login` to get an access token
3. **Use the token** in the Authorization header:
   ```bash
   Authorization: Bearer <your-jwt-token>
   ```

### Token Format
The JWT token contains:
- `sub`: User's email
- `user_id`: User's unique identifier
- `exp`: Token expiration timestamp

## 🧪 Testing

Run the test suite:

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app

# Run specific test file
pytest tests/test_auth.py
```

## 📝 Logging

The application uses structured logging with different levels:

- **DEBUG**: Detailed information for debugging
- **INFO**: General information about application flow
- **WARNING**: Warning messages for potential issues
- **ERROR**: Error messages for failed operations

Logs are automatically generated for:
- Request/response logging
- Database operations
- Authentication events
- Error handling

## 🔧 Development

### Architecture Overview

The application follows a clean architecture pattern:

1. **Controllers** (`app/controllers/`): Handle HTTP requests and responses
2. **Services** (`app/services/`): Contain business logic
3. **Models** (`app/models/`): Define data structures
4. **Schemas** (`app/schemas/`): Pydantic models for validation
5. **Dependencies** (`app/dependencies/`): FastAPI dependency injection
6. **Database** (`app/database/`): Data persistence layer

### Adding New Endpoints

1. Create a new controller in `app/controllers/`
2. Add business logic in `app/services/`
3. Define schemas in `app/schemas/`
4. Add dependencies in `app/dependencies/` if needed
5. Add tests in `tests/`

### Adding New Models

1. Create the model in `app/models/`
2. Define the schema in `app/schemas/`
3. Add database operations in `app/services/`
4. Create API endpoints in `app/controllers/`

### Database Operations

The application uses an abstract database interface that can be extended to support different databases:

```python
from app.database.base import DatabaseInterface

class YourDatabase(DatabaseInterface):
    async def create(self, collection: str, data: dict, document_id: str = None) -> str:
        # Implementation
        pass
```

## 🚀 Deployment

### Environment Variables for Production

```bash
DEBUG=false
SECRET_KEY="your-production-secret-key"
CORS_ORIGINS=["https://yourdomain.com"]
```

### Health Checks

The application provides health check endpoints:

- `GET /health` - Basic health status
- `GET /` - API information

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:

1. Check the API documentation
2. Review the logs for error details
3. Open an issue on GitHub

## 🔄 Changelog

### Version 1.0.0
- Initial release with modular architecture
- JWT authentication with secure token management
- Firestore integration with abstract database layer
- Comprehensive logging and error handling
- Input validation with Pydantic schemas
- Security utilities and CORS middleware
- Clean separation of concerns with controllers and services
- Dependency injection for better testability
- Docker support for containerized deployment 