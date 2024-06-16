from __future__ import annotations

from dataclasses import dataclass, field
import sys
from typing import Generic, TextIO, TypeVar, Union

from red_utils.core.constants import LOG_DIR
from red_utils.core.dataclass_utils import DictMixin

from .constants import default_color_fmt, default_fmt

@dataclass
class LoguruSinkBase(DictMixin):
    """Base Loguru sink class.

    Define common options for children to inherit from.

    Params:
        sink (str|TextIO): A Loguru sink. Can be a string (i.e. "app.log" for a file at ./app.log) or a Python callable (i.e. sys.stdout).
            [Loguru Docs: sinks](https://loguru.readthedocs.io/en/stable/api/logger.html#sink)
        format (str): A string describing the format for the Loguru logger.
            [Loguru Docs: time formatting](https://loguru.readthedocs.io/en/stable/api/logger.html#time).
            [Loguru Docs: color markup formatting](https://loguru.readthedocs.io/en/stable/api/logger.html#color).
        level (str): A severity level string for the logger. Controls which messages will be outputted. Value will be forced uppercase.
            [Loguru Docs: Severity levels](https://loguru.readthedocs.io/en/stable/api/logger.html#levels)
        colorize (bool): Control whether logger outputs are colorized.
    """

    sink: Union[str, TextIO] = field(default=sys.stdout)
    format: str = field(default=default_fmt)
    level: str = field(default="INFO")
    colorize: bool = field(default=False)

    def __post_init__(self):
        self.level = self.level.upper()


@dataclass
class LoguruSinkDefault(LoguruSinkBase):
    """Default Loguru sink. Defaults to colorized, formatted stdout, level=INFO.

    Use this class as a starting point to create customized Loguru sinks. Create a new class
    by inheriting from this one:

    ``` py linenums="1"
    my_loguru_sink = LoguruSinkDefault(sink=...,level=..., colorize=True)
    ```

    Params:
        sink (str|TextIO): A Loguru sink. Can be a string (i.e. "app.log" for a file at ./app.log) or a Python callable (i.e. sys.stdout).
            [Loguru Docs: sinks](https://loguru.readthedocs.io/en/stable/api/logger.html#sink)
        format (str): A string describing the format for the Loguru logger.
            [Loguru Docs: time formatting](https://loguru.readthedocs.io/en/stable/api/logger.html#time).
            [Loguru Docs: color markup formatting](https://loguru.readthedocs.io/en/stable/api/logger.html#color).
        level (str): A severity level string for the logger. Controls which messages will be outputted. Value will be forced uppercase.
            [Loguru Docs: Severity levels](https://loguru.readthedocs.io/en/stable/api/logger.html#levels)
        colorize (bool): Control whether logger outputs are colorized.
    """

    pass


@dataclass
class LoguruSinkStdOut(LoguruSinkBase, DictMixin):
    """Console STDOUT sink.

    Params:
        format (str): A formatted string for log messages
        colorize (bool): If `True`, log messages will be colorized
    """

    format: str = field(default=default_color_fmt)
    colorize: bool = field(default=True)


@dataclass
class LoguruSinkStdErr(LoguruSinkBase):
    """Console STDERR sink.

    Params:
        sink (str, TextIO): the Loguru sink definition
        format (str): A formatted string for log messages
        colorize (bool): If `True`, log messages will be colorized
    """

    sink: Union[str, TextIO] = field(default=sys.stderr)
    format: str = field(default=default_color_fmt)
    colorize: bool = field(default=True)


@dataclass
class LoguruSinkFileBase(DictMixin):
    """Base class for file sinks.

    Params:
        sink (str, TextIO): the Loguru sink definition
        colorize (bool): If `True`, log messages will be colorized
        retention (str|int): Amount of time to retain log files
        rotation (str): Size limit when a log file will be rotated
        format (str): A formatted string for log messages
        level (str): Level of logs to log to file, i.e. `"INFO"`, `"DEBUG"`, etc
        enqueue (bool): Set to `True` if app is asynchronous in order to avoid IO
            collisions
    """

    sink: Union[str, TextIO] = field(default=f"{LOG_DIR}/app.log")
    colorize: bool = field(default=True)
    retention: Union[str, int] = field(default=3)
    rotation: str = field(default="5 MB")
    format: str = field(default=default_fmt)
    level: str = field(default="DEBUG")
    enqueue: bool = field(default=True)


@dataclass
class LoguruSinkFileDefault(LoguruSinkFileBase):
    """Default Loguru file sink. Defaults to file `app.log`, `level=DEBUG`.

    Use this class as a starting point to create customized Loguru file sinks. Create a new class
    by inheriting from this one:

    ``` py linenums="1"
    my_loguru_file_sink = LoguruSinkFileDefault(sink=...,level=..., colorize=True)
    ```

    Params:
        sink (str, TextIO): the Loguru sink definition
        colorize (bool): If `True`, log messages will be colorized
        retention (str|int): Amount of time to retain log files
        rotation (str): Size limit when a log file will be rotated
        format (str): A formatted string for log messages
        level (str): Level of logs to log to file, i.e. `"INFO"`, `"DEBUG"`, etc
        enqueue (bool): Set to `True` if app is asynchronous in order to avoid IO
            collisions
    """

    pass


@dataclass
class LoguruSinkAppFile(LoguruSinkFileBase, DictMixin):
    """Sink class for app.log file.

    Params:
        sink (str, TextIO): the Loguru sink definition
        colorize (bool): If `True`, log messages will be colorized
        retention (str|int): Amount of time to retain log files
        rotation (str): Size limit when a log file will be rotated
        format (str): A formatted string for log messages
        level (str): Level of logs to log to file, i.e. `"INFO"`, `"DEBUG"`, etc
        enqueue (bool): Set to `True` if app is asynchronous in order to avoid IO
            collisions
    """

    pass


@dataclass
class LoguruSinkErrFile(LoguruSinkFileBase):
    """Sink class for error.log file.

    Params:
        sink (str, TextIO): the Loguru sink definition
        colorize (bool): If `True`, log messages will be colorized
        retention (str|int): Amount of time to retain log files
        rotation (str): Size limit when a log file will be rotated
        format (str): A formatted string for log messages
        level (str): Level of logs to log to file, i.e. `"INFO"`, `"DEBUG"`, etc
        enqueue (bool): Set to `True` if app is asynchronous in order to avoid IO
            collisions
    """

    sink: Union[str, TextIO] = field(default=f"{LOG_DIR}/error.log")
    level: str = field(default="ERROR")


@dataclass
class LoguruSinkTraceFile(LoguruSinkFileBase):
    """Sink class for trace.log file.

    Params:
        sink (str, TextIO): the Loguru sink definition
        colorize (bool): If `True`, log messages will be colorized
        retention (str|int): Amount of time to retain log files
        rotation (str): Size limit when a log file will be rotated
        format (str): A formatted string for log messages
        level (str): Level of logs to log to file, i.e. `"INFO"`, `"DEBUG"`, etc
        enqueue (bool): Set to `True` if app is asynchronous in order to avoid IO
            collisions
    """

    sink: Union[str, TextIO] = field(default=f"{LOG_DIR}/trace.log")
    level: str = field(default="TRACE")
    filter: str = field(default="TRACE")
    backtrace: bool = field(default=True)
    diagnose: bool = field(default=True)


## stderr, no color
default_stderr_sink: LoguruSinkStdErr = LoguruSinkStdErr().as_dict()

## stderr, colorized
default_stderr_no_color_sink: LoguruSinkStdErr = LoguruSinkStdErr(
    colorize=False
).as_dict()

## stdout, no color
default_stdout_sink: LoguruSinkStdOut = LoguruSinkStdOut().as_dict()

## stdout, colorized
default_stdout_no_color_sink: LoguruSinkStdOut = LoguruSinkStdOut(
    colorize=False
).as_dict()

## logs/app.log file
default_app_log_file_sink: LoguruSinkAppFile = LoguruSinkAppFile().as_dict()

## logs/error.log file
default_error_log_file_sink: LoguruSinkErrFile = LoguruSinkErrFile().as_dict()

## logs/trace.log file
default_trace_log_file_sink: LoguruSinkTraceFile = LoguruSinkTraceFile().as_dict()


class DefaultSinks(LoguruSinkBase):
    """Return initialized defaults for Loguru sink classes.

    Access initialized sinks as class parameters. For example, to get an STDOUT logger,
    initialized with the default LoguruSinkStdOut settings: `DefaultSinks().stdout`

    To get a list of initialized default sinks (an `app.log`, `err.log`, and `STDOUT` logger), choose
    from `.color` (for loggers initialized with colorize; excludes file loggers), or `.nocolor` (no colorize initialized):

    `DefaultSinks().stdout.color`
    """

    stdout: LoguruSinkStdOut | None = default_stdout_sink
    stderr: LoguruSinkStdErr | None = default_stderr_sink
    log_file: LoguruSinkAppFile | None = default_app_log_file_sink
    error_log_file: LoguruSinkErrFile | None = default_error_log_file_sink
    trace_log_file: LoguruSinkTraceFile | None = default_trace_log_file_sink

    @property
    def color(
        self,
    ) -> list[dict]:
        """List of initialized Loguru loggers.

        Returns:
            (list[dict]): List of Loguru sink dicts with `colorize=True`.

        """
        sink_list = [
            self.stdout,
            self.log_file,
            self.error_log_file,
            self.trace_log_file,
        ]

        return sink_list

    @property
    def no_color(
        self,
    ) -> list[dict]:
        """List of initialized Loguru loggers.

        Returns:
            (list[dict]): List of Loguru sink dicts with `colorize=False`.

        """
        sink_list = [
            default_stdout_no_color_sink,
            self.log_file,
            self.error_log_file,
            self.trace_log_file,
        ]

        return sink_list


default_sinks: list[dict] = DefaultSinks().color
default_sinks_no_color: list[dict] = DefaultSinks().no_color
