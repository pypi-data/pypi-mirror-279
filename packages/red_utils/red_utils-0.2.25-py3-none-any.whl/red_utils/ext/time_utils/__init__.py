"""Utilities for the `pendulum` library."""

from __future__ import annotations

from importlib.util import find_spec

from red_utils.exc import MissingDependencyException

if find_spec("pendulum"):
    from . import pendulum_utils
    from .pendulum_utils import get_ts
    from .pendulum_utils.constants import (
        DEFAULT_TZ,
        TIME_FMT_12H,
        TIME_FMT_24H,
        TS_STR_REPLACE_MAP,
        VALID_TIME_PERIODS,
    )
    from .pendulum_utils.validators import validate_time_period
