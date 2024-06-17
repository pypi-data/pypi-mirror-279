"""Functions to validate inputs for other `red_utils.std.list_utils` methods."""

from __future__ import annotations

import logging

log = logging.getLogger("red_utils.std.list_utils")

import typing as t

def validate_list(_list: list[t.Any] = None) -> list[t.Any]:
    """Validate an input_list.

    Params:
        _list (list): The Python `list` to validate

    Returns:
        (list): A validated `list`.

    """
    assert _list is not None, ValueError("Missing list to evaluate")
    assert isinstance(_list, list), TypeError(
        f"Invalid type for input _list: ({type(_list)}). Must be a list."
    )

    return _list
