import logging
import os
from logging import FileHandler, Formatter


def setup_logging(log_file: str = "logs/trading_bot.log"):
    os.makedirs(os.path.dirname(log_file) or "logs", exist_ok=True)

    # Use the root logger so module loggers propagate automatically
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # Clear existing handlers to avoid duplicates and ensure no console logging
    if logger.handlers:
        logger.handlers.clear()

    # File handler only
    file_handler = FileHandler(log_file)
    formatter = Formatter("%(asctime)s | %(levelname)s | %(name)s | %(message)s")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger
