<<<<<<< HEAD
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

from config.settings import settings


def configure_logging() -> logging.Logger:
    """Configure and return the Dart Vader application logger."""

    log_directory = Path("logs")
    log_directory.mkdir(parents=True, exist_ok=True)

    logger = logging.getLogger("dart_vader")

    if logger.handlers:
        return logger

    level = getattr(logging, settings.log_level, logging.INFO)
    logger.setLevel(level)

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    file_handler = RotatingFileHandler(
        log_directory / "bot.log",
        maxBytes=5_000_000,
        backupCount=5,
        encoding="utf-8",
    )
    file_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger


=======
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

from config.settings import settings


def configure_logging() -> logging.Logger:
    """Configure and return the Dart Vader application logger."""

    log_directory = Path("logs")
    log_directory.mkdir(parents=True, exist_ok=True)

    logger = logging.getLogger("dart_vader")

    if logger.handlers:
        return logger

    level = getattr(logging, settings.log_level, logging.INFO)
    logger.setLevel(level)

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    file_handler = RotatingFileHandler(
        log_directory / "bot.log",
        maxBytes=5_000_000,
        backupCount=5,
        encoding="utf-8",
    )
    file_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger


>>>>>>> 70ee258 (Connecting traspberry pi and fix minor version compatability issues)
logger = configure_logging()