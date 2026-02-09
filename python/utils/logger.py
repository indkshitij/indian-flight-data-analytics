import logging
import os
from datetime import datetime


def get_logger(name: str, log_level=logging.INFO):
    """
    Creates and returns a configured logger.

    Parameters:
    - name: Logger name (usually __name__)
    - log_level: logging.INFO / DEBUG / ERROR

    Returns:
    - logger object
    """

    # Create logs directory if not exists
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)

    # Log file name with date
    log_file = os.path.join(
        log_dir, f"flight_analysis_{datetime.now().strftime('%Y%m%d')}.log"
    )

    logger = logging.getLogger(name)
    logger.setLevel(log_level)

    # Prevent duplicate handlers (important in notebooks)
    if logger.handlers:
        return logger

    # Formatter
    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    # File handler
    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger
