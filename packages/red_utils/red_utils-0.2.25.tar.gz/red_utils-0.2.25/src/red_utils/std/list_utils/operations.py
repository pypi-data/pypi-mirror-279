from __future__ import annotations

import logging

log = logging.getLogger("red_utils.std.list_utils")

import random
import typing as t

from .validators import validate_list

def select_random_from_list(lst: list[t.Any] = None) -> t.Any:
    """Return a randomly selected item from the list.

    Params:
        lst (list): The Python list to select from.

    Returns:
        (Any): An object from the original list.

    """
    validate_list(lst)

    rand_index: int = random.randint(0, len(lst) - 1)

    return lst[rand_index]
