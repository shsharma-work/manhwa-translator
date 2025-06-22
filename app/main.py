from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.api import auth, users
from app.config import settings
import uvicorn

# Create FastAPI app
app = FastAPI(
    title="Manhwa Translator API",
    description="A professional FastAPI application for user authentication with Firestore database integration",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(users.router)


@app.get("/", tags=["root"])
async def root():
    """
    Root endpoint
    
    Returns a welcome message and API information.
    """
    return {
        "message": "Welcome to Manhwa Translator API",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc"
    }


@app.get("/health", tags=["health"])
async def health_check():
    """
    Health check endpoint
    
    Returns the health status of the API.
    """
    return {
        "status": "healthy",
        "message": "API is running successfully"
    }


@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """
    Custom HTTP exception handler
    """
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """
    General exception handler
    """
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )


if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug
    ) 