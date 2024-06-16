"""Handlers defined in this file can be imported and used as `with` context managers.
"""

from __future__ import annotations

import logging

log = logging.getLogger("red_utils.ext.context_managers.cli_spinners.handlers")

from contextlib import contextmanager
import time

import rich
from rich.console import Console

@contextmanager
def SimpleSpinner(message: str = "Loading..."):
    """Get a simple CLI spinner context manager.

    Params:
        message (str): The message to display while the spinner is running

    Usage:

    ``` py linenums="1"
    with SimpleSpinnner("Your message... "):
        ...
    ```
    """
    rich_console: Console = Console()

    try:
        with rich_console.status(message) as status:
            yield status
    except Exception as exc:
        msg = Exception(f"Unhandled exception yielding spinner. Details: {exc}")
        log.error(msg)

        raise exc
    finally:
        # rich_console.clear()
        rich_console.clear_live()
