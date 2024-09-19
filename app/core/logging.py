import sys

from loguru import logger

from core.settings import settings

logger.remove()
logger.add(
    sys.stdout,
    format=settings.LOGGER_FORMAT,
    enqueue=True,
)
logger.add(
    settings.LOGGER_FILENAME,
    format=settings.LOGGER_FORMAT,
    enqueue=True,
)

__all__ = ["logger"]
