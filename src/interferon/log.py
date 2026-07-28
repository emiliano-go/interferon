"""Centralized logging"""

import logging
import sys
from typing import Literal


LogLevel = int | Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]

def setup_logging(level : LogLevel = logging.INFO) -> None:
    """Configure root logger once. Call once at entrypoint."""

    if isinstance(level, str):
        level = getattr(logging, level.upper())

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter(
        "%(asctime)s  %(levelname)-8s  %(name)s  %(message)s",
        datefmt="%H:%M:%S",
        )
    )

    root = logging.getLogger()
    root.setLevel(level)
    root.addHandler(handler)


def get_logger(name : str) -> logging.Logger:
    """Get a logger. Pass __name__ from the calling module"""

    return logging.getLogger(name)

