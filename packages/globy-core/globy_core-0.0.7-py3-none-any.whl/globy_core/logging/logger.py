import logging
import colorlog
from time import time

GLOBY_LOGGER = "GlobyLogger"  # Logger name to provide in your applications

class Logger:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Logger, cls).__new__(cls)
            cls._instance._initialize_logger()
        return cls._instance

    def _initialize_logger(self):
        self.logger = logging.getLogger(GLOBY_LOGGER)
        log_handler = colorlog.StreamHandler()
        log_handler.setFormatter(
            colorlog.ColoredFormatter(
                "%(log_color)s%(levelname)s:%(name)s:%(message)s",
                log_colors={
                    "DEBUG": "cyan",
                    "INFO": "white",
                    "WARNING": "yellow",
                    "ERROR": "red",
                    "CRITICAL": "red,bg_white",
                },
            )
        )
        self.logger.addHandler(log_handler)
        self.logger.setLevel(logging.WARNING)

    def set_log_level(self, loglevel):
        if loglevel == 1:
            self.logger.setLevel(logging.ERROR)
        elif loglevel == 2:
            self.logger.setLevel(logging.INFO)
        elif loglevel == 3:
            self.logger.setLevel(logging.DEBUG)