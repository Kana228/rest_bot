"""
Logging configuration for the bot
"""
import logging
import os
from logging.handlers import RotatingFileHandler
from pathlib import Path

def setup_logging():
    """Setup logging configuration"""
    # Create logs directory if it doesn't exist
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    # Get log level from environment
    log_level = os.getenv("LOG_LEVEL", "INFO").upper()
    log_file = os.getenv("LOG_FILE", "logs/bot.log")
    
    # Configure root logger
    logging.basicConfig(
        level=getattr(logging, log_level),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            # Console handler
            logging.StreamHandler(),
            # File handler with rotation
            RotatingFileHandler(
                log_file,
                maxBytes=10*1024*1024,  # 10MB
                backupCount=5,
                encoding='utf-8'
            )
        ]
    )
    
    # Set specific logger levels
    logging.getLogger('aiogram').setLevel(logging.INFO)
    logging.getLogger('urllib3').setLevel(logging.WARNING)
    
    # Create logger for the bot
    logger = logging.getLogger('rest_bot')
    logger.info(f"Logging configured with level: {log_level}")
    
    return logger
