import logging
import sys

from app.core.config import get_settings

settings = get_settings()


def setup_logging() -> None:
    """
    Configure application logging.
    """

    logging.basicConfig(
        level=getattr(logging, settings.log_level.upper(), logging.INFO),
        format=(
            "%(asctime)s | "
            "%(levelname)-8s | "
            "%(name)s | "
            "%(message)s"
        ),
        handlers=[
            logging.StreamHandler(sys.stdout),
        ],
        force=True,
    )


def get_logger(name: str) -> logging.Logger:
    """
    Return a configured logger instance.
    """
    return logging.getLogger(name)