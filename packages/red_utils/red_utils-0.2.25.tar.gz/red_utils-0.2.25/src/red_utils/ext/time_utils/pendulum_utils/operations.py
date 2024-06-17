from __future__ import annotations

import logging

log = logging.getLogger("red_utils.ext.time_utils.pendulum_utils")

from typing import Union

from red_utils.exc import MissingDependencyException

from .constants import (
    DEFAULT_TZ,
    TIME_FMT_12H,
    TIME_FMT_24H,
    TS_STR_REPLACE_MAP,
)
from .validators import VALID_TIME_PERIODS

try:
    import pendulum

    PENDULUM_AVAILABLE = True
except ImportError:
    PENDULUM_AVAILABLE = False

    raise MissingDependencyException(
        msg="Could not import time_utils module. Missing dependencies.",
        missing_dependencies=["pendulum"],
    )


def get_ts(
    tz: str = DEFAULT_TZ,
    as_str: bool = False,
    str_fmt: str = TIME_FMT_24H,
    safe_str: bool = False,
    char_replace_map: list[dict] = TS_STR_REPLACE_MAP,
) -> Union[str, pendulum.DateTime]:
    """Return a `pendulum.DateTime` object of the current time.

    Optionally return timestamp as a string.

    Params:
        tz (str): Unix timezone string, defaults to `'America/New_York'`.
            **Note**: [Unix timezone strings](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones)
        as_str (bool): If `True`, returns timestamp as a string instead of `DateTime`.
        str_fmt (str): String that defines the format of the timestamp if `as_str=True`.
            **Note**: [Pendulum Docs: String Formatting](https://pendulum.eustace.io/docs/#string-formatting)
        safe_str (bool): If `True`, replaces characters (like `':'` and `' '`) with a string value that is safe
            to use in a terminal, as a filename, etc (like `-` and `_`).
        char_replace_map (list[dict]): A list of dicts defining characters to search for and replace
            in the timestamp str.
            Example replace map: `[{"search": ":", "replace": "-"}, {"search": " ", "replace": "_"}]`

    Returns:
        (pendulum.DateTime): A `pendulum.DateTime` object of the current time
        (str): If `as_str=True`, returns a string representation of the `pendulum.DateTime` timestamp, formatted by `str_fmt`

    """
    now: pendulum.DateTime = pendulum.now(tz=tz)

    if not as_str:
        return now
    else:
        if safe_str:
            str_fmt

            for r in char_replace_map:
                str_fmt = str_fmt.replace(r["search"], r["replace"])

        now_fmt: str = now.format(fmt=str_fmt)

        return now_fmt
