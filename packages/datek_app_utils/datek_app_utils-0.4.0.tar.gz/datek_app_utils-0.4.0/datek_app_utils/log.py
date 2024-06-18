import sys
from logging import INFO, Formatter, Handler, Logger, StreamHandler, getLogger


class LogHandler:
    _handler: Handler = StreamHandler(stream=sys.stdout)

    @classmethod
    def set(cls, handler: Handler):
        cls._handler = handler

    @classmethod
    def get(cls) -> Handler:
        return cls._handler


class LogLevel:
    _log_level: int = INFO

    @classmethod
    def set(cls, level: int):
        cls._log_level = level

    @classmethod
    def get(cls) -> int:
        return cls._log_level


class LogFormatter:
    _formatter: Formatter = Formatter(
        "%(asctime)s [%(filename)s:%(lineno)d] %(levelname)-8s %(message)s"
    )

    @classmethod
    def set(cls, formatter: Formatter):
        cls._formatter = formatter
        LogHandler.get().setFormatter(formatter)

    @classmethod
    def get(cls) -> Formatter:
        return cls._formatter


LogHandler.get().setFormatter(LogFormatter.get())


def create_logger(name: str) -> Logger:
    logger = getLogger(name)
    logger.addHandler(LogHandler.get())
    logger.setLevel(LogLevel.get())

    return logger
