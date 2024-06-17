from __future__ import annotations

from .constants import VALID_TIME_PERIODS

def validate_time_period(period: str = None) -> str:
    """Validate a time period string.

    Pass a time period (i.e. "days", "weeks", etc). If the period
    matches a valid time period, string is returned, otherwise a
    ValueError is raised.

    Params:
        period (str): A period of time, like 'days' or 'weeks'
    """
    if period is None:
        raise ValueError("Missing a time period to evaluate")
    if not isinstance(period, str):
        raise TypeError(
            f"Invalid type for time period: ({type(period)}). Must be one of {VALID_TIME_PERIODS}"
        )
    if period not in VALID_TIME_PERIODS:
        raise ValueError(
            f"Invalid time period: '{period}'. Must be one of {VALID_TIME_PERIODS}"
        )

    return period
