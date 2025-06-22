#!/usr/bin/env python3
"""
Run script for the Manhwa Translator API.
"""
import uvicorn
from app.core.config import settings
from app.core.logging import get_logger

logger = get_logger(__name__)

if __name__ == "__main__":
    logger.info(f"🚀 Starting {settings.app_name}...")
    logger.info(f"📡 Server will be available at: http://{settings.server.host}:{settings.server.port}")
    logger.info(f"📚 API Documentation: http://{settings.server.host}:{settings.server.port}/docs")
    logger.info(f"📖 Alternative Docs: http://{settings.server.host}:{settings.server.port}/redoc")
    logger.info(f"🔧 Debug mode: {settings.server.debug}")
    logger.info("=" * 50)
    
    uvicorn.run(
        "app.main:app",
        host=settings.server.host,
        port=settings.server.port,
        reload=settings.server.debug,
        log_level="info"
    ) 