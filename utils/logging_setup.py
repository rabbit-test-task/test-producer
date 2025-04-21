import logging
import sys
from config.settings import LoggingSettings

def configure_logging(config: LoggingSettings) -> None:
    """Configure logger with settings"""

    log_level = config.level.upper()
    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, log_level))
    
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(getattr(logging, log_level))
    
    formatter = logging.Formatter(log_format)
    console_handler.setFormatter(formatter)
    
    root_logger.handlers.clear()
    root_logger.addHandler(console_handler)
    
    logging.getLogger("aio_pika").setLevel(logging.WARNING)
    logging.getLogger("aiormq").setLevel(logging.WARNING)
    
    logging.info(f"Logger initialized with level: {log_level}")