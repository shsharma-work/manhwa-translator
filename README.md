# Manhwa Translator API

A professional FastAPI application for user authentication with Firestore database integration.

## Features

- User registration and authentication
- JWT token-based authentication
- Firestore database integration
- Password hashing with bcrypt
- Input validation with Pydantic
- Professional project structure

## Project Structure

```
manhwa-translator/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   ├── database/
│   │   ├── __init__.py
│   │   └── firestore.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── user.py
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── user.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   └── user.py
│   └── api/
│       ├── __init__.py
│       ├── auth.py
│       └── users.py
├── tests/
│   ├── __init__.py
│   ├── test_auth.py
│   └── test_users.py
├── env.example
├── requirements.txt
├── setup_firebase.py
└── README.md
```

## Quick Start

1. **Clone and setup**
   ```bash
   git clone <repository-url>
   cd manhwa-translator
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Setup Firebase (Easy way)**
   ```bash
   python setup_firebase.py
   ```
   Follow the interactive guide to configure Firebase.

3. **Run the application**
   ```bash
   python run.py
   ```

## Detailed Setup Instructions

### 1. Firebase Configuration

**Option A: Using the Setup Script (Recommended)**
```bash
python setup_firebase.py
```

**Option B: Manual Setup**
1. Create a Firebase project named "manhwa-translator-422ed" at [Firebase Console](https://console.firebase.google.com/)
2. Enable Firestore Database
3. Download your service account key JSON file
4. Rename it to `firebase-service-account.json` and place it in the project root

### 2. Environment Configuration
```bash
cp env.example .env
```
Edit `.env` file with your configuration:
```
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
FIREBASE_PROJECT_ID=manhwa-translator-422ed
```

### 3. Run the Application
```bash
python run.py
# or
uvicorn app.main:app --reload
```

### 4. Access the API
- API Documentation: http://localhost:8000/docs
- Alternative Docs: http://localhost:8000/redoc

## API Endpoints

### Authentication
- `POST /auth/register` - Register a new user
- `POST /auth/login` - Login user and get access token

### Users
- `GET /users/me` - Get current user profile (requires authentication)

## Testing

Run tests with pytest:
```bash
pytest
```

## Environment Variables

- `SECRET_KEY`: Secret key for JWT token signing
- `ALGORITHM`: JWT algorithm (default: HS256)
- `ACCESS_TOKEN_EXPIRE_MINUTES`: Token expiration time in minutes
- `FIREBASE_PROJECT_ID`: Firebase project ID (default: manhwa-translator-422ed)

## Security Features

- Password hashing with bcrypt
- JWT token authentication
- Input validation with Pydantic
- Secure password requirements
- Rate limiting (can be added)

## Firebase Project Requirements

- **Project Name**: manhwa-translator-422ed
- **Database**: Firestore (NoSQL)
- **Authentication**: Service Account Key
- **Collections**: users (automatically created)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request 