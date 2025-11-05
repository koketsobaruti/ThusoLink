# src/backend/utils/logger_utils.py
import logging
from typing import Optional

class LoggerUtils:
    @staticmethod
    def get_logger(name: Optional[str] = None, level: int = logging.INFO) -> logging.Logger:
        """
        Returns a configured logger instance.

        Args:
            name (str, optional): Logger name. Defaults to __name__.
            level (int, optional): Logging level. Defaults to logging.INFO.

        Returns:
            logging.Logger: Configured logger instance
        """
        logger_name = name or __name__
        logger = logging.getLogger(logger_name)

        if not logger.handlers:
            # Configure basic logging only if not already configured
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S"
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            logger.setLevel(level)
            logger.propagate = False

        return logger
