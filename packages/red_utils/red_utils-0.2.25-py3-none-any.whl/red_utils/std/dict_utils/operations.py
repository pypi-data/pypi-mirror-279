from __future__ import annotations

import logging

log = logging.getLogger("red_utils.std.dict_utils")

from typing import Any

from .validators import validate_dict

def debug_dict(in_dict: dict = None) -> None:
    """Debug print a dict by looping overkeys and printing.

    If type of key is also dict, re-run the loop on that key and continue.

    Params:
        in_dict (dict): The input dict to loop & debug print

    Raises:
        Exception: A generic `Exception` whenever debug printing a `dict` fails

    """
    validate_dict(in_dict)

    try:
        for k in in_dict.keys():
            if not isinstance(in_dict[k], dict):
                print(f"Key [{k}]:\n\tType: {type(in_dict[k])}\n\tValue: {in_dict[k]}")
            else:
                print(f"Key [{k}] is type dict. Looping over sub-dict")
                debug_dict(in_dict=in_dict[k])

                continue

    except Exception as exc:
        msg = Exception(
            f"Unhandled exception looping dict. Errored on key {k}. Details: {exc}"
        )
        log.error(msg)

        raise exc


def merge_dicts(
    original_dict: dict[str, Any] = None,
    update_vals: dict[str, Any] = None,
) -> dict[str, str]:
    """Merge dicts into new dict.

    Params:
        original_dict (dict): The first `dict`
        update_vals (dict): The new `dict` to be merged into the first `dict`.

    Returns:
        (dict): A merged `dict` from the 2 input `dict`s


    Raises:
        Exception: When merging the `dict`s fails

    """
    validate_dict(original_dict)
    validate_dict(update_vals)

    try:
        _new: dict = {**update_vals, **original_dict}

    except Exception as exc:
        msg = Exception(f"Unhandled exception merging dicts. Details: {exc}")
        log.error(msg)

        raise exc

    return _new


def update_dict(
    original_dict: dict[str, Any] = None,
    update_vals: dict[str, Any] = None,
) -> dict[str, str]:
    """Update a dict with values from a second dict.

    Params:
        original_dict: The original dictionary to be updated.
        update_vals: The dict with values with which to update the original dict.

    Returns:
        (dict): A `dict` with updated values

    """
    validate_dict(original_dict)
    validate_dict(update_vals)

    try:
        ## Create a copy of original_dict to update
        new_dict: dict[str, str] = original_dict.copy()
        ## Update new_dict with update_vals dict
        new_dict.update(update_vals)

        return new_dict

    except Exception as exc:
        msg = Exception(f"Unhandled exception updating dict. Details: {exc}")
        log.error(msg)

        raise exc
