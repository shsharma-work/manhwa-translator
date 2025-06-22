"""
Main FastAPI application for the Manhwa Translator API.
"""
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.core.config import settings
from app.core.logging import get_logger
from app.core.exceptions import ManhwaTranslatorException
from app.middleware.cors import get_cors_config
from app.middleware.logging import LoggingMiddleware
from app.controllers import auth_controller, user_controller

logger = get_logger(__name__)


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    app = FastAPI(
        title=settings.app_name,
        description=settings.app_description,
        version=settings.app_version,
        docs_url="/docs",
        redoc_url="/redoc"
    )
    
    # Add CORS middleware
    cors_config = get_cors_config()
    app.add_middleware(
        CORSMiddleware,
        allow_origins=cors_config["allow_origins"],
        allow_credentials=cors_config["allow_credentials"],
        allow_methods=cors_config["allow_methods"],
        allow_headers=cors_config["allow_headers"],
    )
    
    # Add logging middleware
    app.add_middleware(LoggingMiddleware)
    
    # Include routers
    app.include_router(auth_controller.router)
    app.include_router(user_controller.router)
    
    # Add exception handlers
    app.add_exception_handler(ManhwaTranslatorException, handle_manhwa_exception)
    app.add_exception_handler(HTTPException, handle_http_exception)
    app.add_exception_handler(Exception, handle_general_exception)
    
    return app


def handle_manhwa_exception(request: Request, exc: ManhwaTranslatorException) -> JSONResponse:
    """Handle custom Manhwa Translator exceptions."""
    logger.error(f"Manhwa Translator exception: {exc.message}")
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "detail": exc.message,
            "details": exc.details
        }
    )


def handle_http_exception(request: Request, exc: HTTPException) -> JSONResponse:
    """Handle HTTP exceptions."""
    logger.warning(f"HTTP exception: {exc.status_code} - {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )


def handle_general_exception(request: Request, exc: Exception) -> JSONResponse:
    """Handle general exceptions."""
    logger.error(f"General exception: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )


# Create the application instance
app = create_app()


@app.get("/", tags=["root"])
async def root():
    """
    Root endpoint.
    
    Returns a welcome message and API information.
    """
    logger.debug("Root endpoint accessed")
    return {
        "message": f"Welcome to {settings.app_name}",
        "version": settings.app_version,
        "docs": "/docs",
        "redoc": "/redoc"
    }


@app.get("/health", tags=["health"])
async def health_check():
    """
    Health check endpoint.
    
    Returns the health status of the API.
    """
    logger.debug("Health check endpoint accessed")
    return {
        "status": "healthy",
        "message": "API is running successfully",
        "version": settings.app_version
    }


if __name__ == "__main__":
    import uvicorn
    
    logger.info(f"Starting {settings.app_name}...")
    logger.info(f"Server will be available at: http://{settings.server.host}:{settings.server.port}")
    logger.info(f"Debug mode: {settings.server.debug}")
    
    uvicorn.run(
        "app.main:app",
        host=settings.server.host,
        port=settings.server.port,
        reload=settings.server.debug,
        log_level="info"
    ) 