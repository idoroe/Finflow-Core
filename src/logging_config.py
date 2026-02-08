"""
logging_config.py — Sets up logging for the entire pipeline.

HIGH-LEVEL EXPLANATION:
    Instead of using print() everywhere, we use Python's logging module.
    This gives us timestamps, severity levels (INFO, WARNING, ERROR), and
    the ability to write logs to both the terminal AND a file.

WHY THIS MATTERS AT RBC:
    In production pipelines, print() is useless — logs are how you debug failures
    at 3 AM. Every enterprise pipeline uses structured logging so you can search
    and filter what happened, when, and where.
"""

import logging
import sys


def setup_logging(level: str = "INFO") -> logging.Logger:
    """Configure and return the root logger for the pipeline.

    Args:
        level: Logging level — "DEBUG" shows everything, "INFO" shows normal
               operations, "WARNING" and above show only problems.

    Returns:
        A configured logger you can use like: logger.info("Loaded 500 rows")
    """
    logger = logging.getLogger("finflow")
    logger.setLevel(getattr(logging, level.upper(), logging.INFO))

    # Avoid adding duplicate handlers if setup_logging is called multiple times
    if logger.handlers:
        return logger

    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Handler 1: print to terminal (stdout)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger
