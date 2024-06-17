"""Utilities, constants, & classes for the `pendulum` library."""

from __future__ import annotations

from importlib.util import find_spec

from red_utils.exc import MissingDependencyException

try:
    if find_spec("pendulum"):
        from .constants import (
            DEFAULT_TZ,
            TIME_FMT_12H,
            TIME_FMT_24H,
            TS_STR_REPLACE_MAP,
        )
        from .operations import get_ts
        from .validators import VALID_TIME_PERIODS
except ModuleNotFoundError as mod_err:
    msg = MissingDependencyException(
        msg="Could not import time_utils due to missing dependencies.",
        missing_dependencies=["pendulum"],
    )

    raise ModuleNotFoundError(msg.exc_msg)
