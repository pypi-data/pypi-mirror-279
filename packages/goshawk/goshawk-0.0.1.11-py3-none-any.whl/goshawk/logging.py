import sys

from loguru import logger as LOG

from . import app_settings

fmt = "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"
LOG.remove()
LOG.add(sys.stderr, colorize=True, level=app_settings.LOG_LEVEL.value, format=fmt)
LOG.debug("Logging enabled")
