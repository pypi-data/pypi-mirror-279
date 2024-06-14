import os, logging
from enum import StrEnum

StrPath = str | os.PathLike[str]

class ConstantsLogger(StrEnum):
    NAME = "LoggerContext"

class Logger:
    """
    # Example of using Logger
    At the root of the project, the logs folder is created and the types of errors are differentiated by different files.
    ```python

    # main.py
    from logyca import Logger, ConstantsLogger
    logger = Logger(logger_name=ConstantsLogger.NAME,log_dir=FOLDER_LOGS,log_file_name=f"{App.Settings.NAME}")
    logger.info(f"message")

    # Other files.py
    from logyca import Logger, ConstantsLogger
    import logging
    logger = logging.getLogger(ConstantsLogger.NAME)

    logger.info(f"message")
    logger.error(f"message")

    ```
    """
    def __init__(
        self,
        logger_name: str,
        log_dir: str,
        log_file_name: str
    ):
        os.makedirs(log_dir, exist_ok=True)
        self.log_dir = log_dir
        self.log_file_name = log_file_name
        self.logger_name = logger_name
        self.logger = logging.getLogger(logger_name)
        self.logger.setLevel(logging.DEBUG)
        self._setup_handlers()

    def _setup_handlers(self) -> None:
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        log_levels = (
            logging.DEBUG,
            logging.INFO,
            logging.WARNING,
            logging.ERROR,
            logging.CRITICAL,
        )
        log_names = ("debug", "info", "warning", "error", "critical")

        for level, name in zip(log_levels, log_names):
            log_file = os.path.join(self.log_dir, f"{self.log_file_name}.{name}.log")
            handler = logging.FileHandler(log_file)
            handler.setFormatter(formatter)
            handler.setLevel(level)
            handler.filter = lambda record, level=level: record.levelno == level
            self.logger.addHandler(handler)

    def debug(self, message: object) -> None:
        self.logger.debug(message)

    def info(self, message: object) -> None:
        self.logger.info(message)

    def warning(self, message: object) -> None:
        self.logger.warning(message)

    def error(self, message: object) -> None:
        self.logger.error(message)

    def critical(self, message: object) -> None:
        self.logger.critical(message)
