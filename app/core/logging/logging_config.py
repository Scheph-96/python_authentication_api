import logging
import sys
import structlog
from structlog.stdlib import ProcessorFormatter
from logging.handlers import RotatingFileHandler
from app.core.config import Settings
from pathlib import Path

def configure_logging():
    """
        When someone logs something, here's how logs should look.
    """
    
    BASE_DIR = Path(__file__).resolve().parent.parent.parent
    LOGS_PATH = BASE_DIR / "logs"
    
    log_level = logging.INFO
    
    # FORMATTERS
    console_formatter = ProcessorFormatter(
        processor=structlog.dev.ConsoleRenderer()
    )
    file_formatter = ProcessorFormatter(
        processor=structlog.processors.JSONRenderer()
    )
    
    # CONSOLE HANDLER
    console_handler = logging.StreamHandler(sys.stdout)
    
    # FILE HANDLER
    file_handler = RotatingFileHandler(
        LOGS_PATH / "app.log", # folder must exist
        maxBytes=10_000_000, # 10 Mb per file
        backupCount=5 # keep 5 old logs
    )
    
    if Settings.ENV == "production":
        console_handler.setFormatter(console_formatter)
        file_handler.setFormatter(file_formatter)
    else:
        console_handler.setFormatter(console_formatter)
    
    # ROUTER LOGGER
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    
    # If we call configure_logging() multiple times (reload, tests), handlers will duplicate and logs will appear multiple times.
    if not root_logger.handlers:
        root_logger.addHandler(console_handler)
        root_logger.addHandler(file_handler)
        
    structlog.configure(
        processors=[
            structlog.processors.add_log_level,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
        ],
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.make_filtering_bound_logger(log_level),
        cache_logger_on_first_use=True,
    )