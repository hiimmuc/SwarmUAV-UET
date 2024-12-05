import logging

from colorlog import ColoredFormatter

# cspell: ignore levelname, asctime LOGFORMAT

LOGFORMAT = "[{asctime}] - {levelname} - {message}"
# formatter = ColoredFormatter(LOGFORMAT)


class Logger:

    def __init__(self) -> None:
        self.logger = logging.getLogger("UAV-logger")
        self.console_handler = logging.StreamHandler()
        self.file_handler = logging.FileHandler("app.log", mode="w", encoding="utf-8")
        self.logger.addHandler(self.console_handler)
        self.logger.addHandler(self.file_handler)
        self.formatter = logging.Formatter(fmt=LOGFORMAT, style="{", datefmt="%Y-%m-%d %H:%M:%S")
        self.console_handler.setFormatter(self.formatter)
        self.logger.setLevel(logging.DEBUG)

    def log(self, message, level="info"):
        level = level.lower()
        if level == "info":
            self.logger.info(message)
        elif level == "warning":
            self.logger.warning(message, exc_info=False)
        elif level == "error":
            self.logger.error(message, exc_info=True)
        elif level == "critical":
            self.logger.critical(message, exc_info=True)
        else:
            self.logger.debug(message, exc_info=False)
