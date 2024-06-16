"""Functions that can be imported and used to manage `loguru`."""

from __future__ import annotations

import logging

log = logging.getLogger("red_utils.ext.loguru_utils")

import datetime
import io
from logging import Handler
from pathlib import Path
import sys
from typing import Callable, Coroutine, Union

from .constants import default_color_fmt, default_fmt
from .sinks import (
    default_app_log_file_sink,
    default_error_log_file_sink,
    default_sinks,
    default_stderr_no_color_sink,
    default_stderr_sink,
    default_stdout_no_color_sink,
    default_stdout_sink,
    default_trace_log_file_sink,
)
from .validators import validate_compression_str, validate_level, validate_logger

from loguru import logger

def add_sink(
    _logger: logger = None,
    sink: Union[str, Path, io.TextIOWrapper, Handler, Callable, Coroutine] = None,
    level: Union[int, str] | None = "INFO",
    format: Union[str, Callable] = default_fmt,
    color_format: Union[str, Callable] = default_color_fmt,
    filter: Union[str, Callable, dict] = None,
    colorize: bool | None = False,
    serialize: bool | None = False,
    backtrace: bool | None = False,
    diagnose: bool | None = False,
    enqueue: bool | None = False,
    catch: bool | None = False,
    rotation: Union[int, datetime.time, datetime.timedelta, str, Callable] = None,
    retention: Union[int, datetime.timedelta, str, Callable] = None,
    compression: Union[str, Callable] = None,
) -> logger:
    """Add a sink to a Loguru logger.

    Helper function for adding a sink to a Loguru logger.
    Can be called without arguments to use a default instance.

    Params:
        _logger (loguru.logger): An instance of `loguru.logger` to add a sink to
        sink (str|Path|io.TextIOWrapper|Handler|Callable|Coroutine): A Loguru-compatible logger sink.
            If the value is a `str` or `Path`, the sink will be a file. Read the
            [Loguru sinks docs](https://loguru.readthedocs.io/en/stable/api/logger.html#sink) for more info,
            or the [Loguru file sink config](https://loguru.readthedocs.io/en/stable/api/logger.html#file) docs.
        level (str): The all-caps log level for the sink, i.e. `"INFO"`, `"DEBUG"`, etc
        format (str|Callable): The formatting for a log message
        color_format (str|Callable): The formatting for a colored log message
        filter (str|Callable, dict): A filter to control messages logged by Loguru
        colorize (bool): If `True`, log messages will be colored using the `color_format`
        serialize (bool): If `True`, log messages will be formatted as json strings
        backtrace (bool): If `True`, errors/traces will print the preceding stack trace that lead to a crash
        diagnose (bool): If `True`, exception trace will display variable values for debugging.
            **Warning**: This should be set to `False` in production to avoid leaking sensitive data.
        enqueue (bool): If using Loguru in an async context, `enqueue` should be set to `True` to avoid IO collisions
            when logging to a file.
        catch (bool): If `True`, errors occurring while sink handles logs messages will be automatically caught, and an
            exception message will be displayed in `sys.stderr`. With this option, the exception is not propagated to
            the caller, preventing your app from crashing.
        rotation (int|datetime.time|datetime.timedelta|str|Callable): Define log rotation rules for file logging
        retention (int|datetime.timedelta|str|Callable): Define how long log files should be retained during rotation
        compression (str|Callable):
    """
    ## Validate inputs
    validate_logger(_logger)
    validate_compression_str(compression, none_ok=True)
    validate_level(level=level)

    if not sink:
        sink: io.TextIOWrapper = sys.stderr

    match colorize:
        case True:
            fmt = color_format
        case False:
            fmt = format

    _logger.add(
        sink=sink,
        level=level,
        format=fmt,
        filter=filter,
        colorize=colorize,
        serialize=serialize,
        backtrace=backtrace,
        diagnose=diagnose,
        enqueue=enqueue,
        catch=catch,
    )

    return _logger


def init_logger(
    sinks: list[dict] = [
        default_stderr_sink,
        default_app_log_file_sink,
        default_error_log_file_sink,
        default_trace_log_file_sink,
    ]
):
    """Initialize a Loguru logger using sink dicts.

    Call this script very early in program execution, ideally as the very first thing to happen.
    To ease with sink configuration, you can import sinks from `red_utils.ext.loguru_utils.sinks`,
    like `LoguruSinkStdOut` which defines a default, colorized `sys.stdout` sink.

    !!! note

        If using a custom `red_utils` sink, when adding it to the list of sinks, use the `.as_dict()`
        function to convert the sink to a dict.

    Example:
        ``` py linenums="1"
        stdout_sink = LoguruSinkStdOut(level="DEBUG")
        init_logger(sinks=[stdout_sink.as_dict()])
        ```

    Params:
        sinks (list[dict]): A list of dicts defining Loguru sinks

    """
    logger.remove()

    for sink in sinks:
        logger.add(**sink)
