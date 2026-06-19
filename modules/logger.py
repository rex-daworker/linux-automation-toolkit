"""logger.py - shared logger for the toolkit (console + file)."""
import logging
import os


def get_logger(log_file="logs/toolkit.log", level="INFO"):
    """Return a shared logger that writes to both the console and a log file."""
    log_dir = os.path.dirname(log_file)
    if log_dir:
        os.makedirs(log_dir, exist_ok=True)

    logger = logging.getLogger("linux_automation_toolkit")
    if not logger.handlers:
        logger.setLevel(getattr(logging, level.upper(), logging.INFO))
        fmt = logging.Formatter(
            "%(asctime)s [%(levelname)s] %(message)s", "%Y-%m-%d %H:%M:%S"
        )
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(fmt)
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(fmt)
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
    return logger
