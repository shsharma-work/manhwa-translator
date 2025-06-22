"""
Logging configuration for the Manhwa Translator API.
"""
import logging
import sys
from typing import Optional
from pathlib import Path
from app.core.config import settings


def setup_logging(
    log_level: str = "INFO",
    log_file: Optional[str] = None,
    log_format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
) -> None:
    """
    Setup logging configuration.
    
    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Optional log file path
        log_format: Log message format
    """
    # Create logs directory if it doesn't exist
    if log_file:
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Configure root logger
    logging.basicConfig(
        level=getattr(logging, log_level.upper()),
        format=log_format,
        handlers=[
            logging.StreamHandler(sys.stdout),
            *([logging.FileHandler(log_file)] if log_file else [])
        ]
    )
    
    # Set specific loggers
    logging.getLogger("uvicorn").setLevel(logging.INFO)
    logging.getLogger("uvicorn.access").setLevel(logging.INFO)
    logging.getLogger("fastapi").setLevel(logging.INFO)
    
    # Create logger for the application
    logger = logging.getLogger("manhwa_translator")
    logger.setLevel(logging.DEBUG if settings.server.debug else logging.INFO)
    
    logger.info(f"Logging configured with level: {log_level}")


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance with the given name.
    
    Args:
        name: Logger name
        
    Returns:
        Logger instance
    """
    return logging.getLogger(f"manhwa_translator.{name}")


# Setup logging on module import
setup_logging() 