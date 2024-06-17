"""Constant values to use as defaults for the `pendulum_utils` module.

Examples:
``` py
TIME_FMT_24H: str = "YYYY-MM-DD HH:MM:SS"
TIME_FMT_12H: str = "YYYY-MM-DD hh:mm:ssA"
DEFAULT_TZ: str = "America/New_York"

TS_STR_REPLACE_MAP = [
    {"search": ":", "replace": "-"},
    {"search": " ", "replace": "_"},
]

VALID_TIME_PERIODS: list[str] = [
    "years",
    "months",
    "weeks",
    "days",
    "hours",
    "minutes",
    "seconds",
]
```

"""

from __future__ import annotations

TIME_FMT_24H: str = "YYYY-MM-DD HH:MM:SS"
TIME_FMT_12H: str = "YYYY-MM-DD hh:mm:ssA"
DEFAULT_TZ: str = "America/New_York"

## Mapping for string character replacement
TS_STR_REPLACE_MAP = [
    {"search": ":", "replace": "-"},
    {"search": " ", "replace": "_"},
]

VALID_TIME_PERIODS: list[str] = [
    "years",
    "months",
    "weeks",
    "days",
    "hours",
    "minutes",
    "seconds",
]
