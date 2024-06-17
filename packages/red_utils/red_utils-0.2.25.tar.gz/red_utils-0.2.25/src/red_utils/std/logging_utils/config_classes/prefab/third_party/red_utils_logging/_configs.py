"""The classes and functions in this file define logging for the `red_utils` library.

If you want to see messages from `red_utils` modules in your app, you will need to add
a logging config by using the methods in this script.
"""

from __future__ import annotations

import logging

log = logging.getLogger(
    "red_utils.std.logging_utils.config_classes.prefab.third_party.red_utils"
)

import typing as t

from red_utils.std.logging_utils.config_classes.formatters import FormatterConfig
from red_utils.std.logging_utils.config_classes.handlers import (
    FileHandlerConfig,
    QueueHandlerConfig,
    QueueListenerConfig,
    RotatingFileHandlerConfig,
    SMTPHandlerConfig,
    SocketHandlerConfig,
    StreamHandlerConfig,
    TimedRotatingFileHandlerConfig,
)
from red_utils.std.logging_utils.config_classes.loggers import (
    LoggerConfig,
    LoggerFactory,
)
from red_utils.std.logging_utils.fmts import (
    DATE_FMT_DATE_ONLY,
    DATE_FMT_STANDARD,
    DATE_FMT_TIME_ONLY,
)
from red_utils.std.logging_utils.fmts._formats import (
    RED_UTILS_DETAIL_FMT,
    RED_UTILS_FMT,
)
from red_utils.std.logging_utils.helpers import (
    get_formatter_config,
    get_logger_config,
    get_rotatingfilehandler_config,
    get_streamhandler_config,
)

def get_red_utils_formatter(
    name: str = "red_utils", fmt: str = RED_UTILS_FMT, datefmt: str = DATE_FMT_STANDARD
) -> FormatterConfig:
    """Return a pre-configured FormatterConfig for the red_utils library.

    Params:
        name (str): The name of the formatter, which you will reference in a handler config.
        fmt (str): The log message format string.
        datefmt (str): The format for timestamps in log messages.

    Returns:
        (FormatterConfig): An initialized FormatterConfig class

    """
    try:
        _formatter: FormatterConfig = get_formatter_config(
            name=name, fmt=fmt, datefmt=datefmt
        )

        return _formatter

    except Exception as exc:
        msg = Exception(
            f"Unhandled exception getting red_utils FormatterConfig. Details: {exc}"
        )
        log.error(msg)

        raise exc


def get_red_utils_console_handler(
    name: str = "red_utils_console",
    level: str = "DEBUG",
    formatter: str = "red_utils",
    filters: list[str] | None = None,
) -> StreamHandlerConfig:
    """Return an initialized StreamHandlerConfig for the red_utils library.

    Params:
        name (str): The name of the handler, which you will reference in a logger config.
        level (str): The log level for the handler (NOTSET, DEBUG, INFO, WARNING, ERROR, CRITICAL).
        formatter (str): The name of the formatter to use. This formatter must exist in the logging dictConfig,
            and can be generated with a FormatterConfig.
        filters (list[str]|None): Optional list of filter function names to apply to the handler.

    Returns:
        (StreamHandlerConfig): An initialized StreamHandlerConfig class.

    """
    try:
        _handler: StreamHandlerConfig = StreamHandlerConfig(
            name=name, level=level.upper(), formatter=formatter, filters=filters
        )

        return _handler

    except Exception as exc:
        msg = Exception(
            f"Unhandled exception getting red_utils StreamHandlerConfig. Details: {exc}"
        )
        log.error(msg)

        raise exc


def get_red_utils_logger(
    name: str = "red_utils",
    handlers: list[str] = ["red_utils_console"],
    level: str = "WARNING",
    propagate: bool = False,
) -> LoggerConfig:
    """Return an initialized LoggerConfig for the red_utils library.

    Params:
        name (str): The name of the logger, which you will reference in a logging config dict.
        handlers (list[str]): A list of handler names for the logger. These loggers must exist in the dictConfig.
        level (str): The log level for the handler (NOTSET, DEBUG, INFO, WARNING, ERROR, CRITICAL).
        propagate (bool): If `False`, logs from this logger will not be propagated down/up to the root logger.

    Returns:
        (LoggerConfig): An initialized LoggerConfig class.

    """
    try:
        _logger: LoggerConfig = get_logger_config(
            name=name, handlers=handlers, level=level.upper(), propagate=propagate
        )

        return _logger

    except Exception as exc:
        msg = Exception(
            f"Unhandled exception getting red_utils LoggerConfig. Details: {exc}"
        )
        log.error(msg)

        raise exc
