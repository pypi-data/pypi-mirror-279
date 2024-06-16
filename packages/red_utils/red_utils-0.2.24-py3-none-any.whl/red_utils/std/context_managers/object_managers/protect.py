"""Context manager classes to protect instances of objects."""

from __future__ import annotations

import inspect
import json
import logging

log = logging.getLogger("red_utils.std.context_managers.object_managers.protect")


class ListProtect:
    """Protect a list during modification by modifying a copy instead of the original.

    ListProtect creates a copy of a list before running operations like .append(), and prevents
    errors on the original object by destroying the copy if an error is encountered, only
    overwriting the original if no errors occur.

    Params:
        original (list): The original Python `list`. A copy will be made during any operations, and will only overwrite
            the original if the operation succeeds.

    Usage:

    ``` py linenums="1"
    ex_list = [1, 2, 3]

    ## Protects from a ZeroDivision error
    with ListProtect(ex_list) as copy:
        copy.append(1/0)

    print(f'List: {ex_list}')
    ```
    """

    def __init__(self, original: list):  # noqa: D107
        ## Call immediately after with ListProtect() as copy.
        if not isinstance(original, list):
            raise TypeError(
                f"Invalid type for protected list: ({type(original)}). Must be of type list."
            )

        ## Set class value to original list
        self.original = original

    def __enter__(self):  # noqa: D105
        ## Call after initializing ListProtect instance.
        ## Create a copy of the list to work on
        self.clone: list = self.original.copy()

        return self.clone

    def __exit__(self, exc_type, exc_value, exc_traceback) -> bool:  # noqa: D105
        ## Call if ListProtect context manager encounters an error.
        ## No exception encountered, update original
        #  list and return
        if exc_type is None:
            self.original[:] = self.clone
        if exc_traceback:
            log.error(exc_traceback)

        ## Error encountered, print details
        else:
            ## https://docs.python.org/3/library/inspect.html?highlight=currentframe
            frame = inspect.currentframe()
            ## Full path to error file
            file_name = frame.f_code.co_filename
            ## Line number where error occurred.
            file_no = frame.f_lineno

            ## Build error details dict
            err = {
                "success": False,
                "detail": {
                    "module": file_name,
                    "line": file_no,
                    "exception_type": exc_type,
                    "exception_text": exc_value,
                },
            }

            ## Return error, exit returning original list
            log.error(
                f"Error encountered running list operation on protected list. Details: \n{err}"
            )

        return True


class DictProtect:
    """Protect a dict during modification by modifying a copy instead of the original.

    DictProtect creates a copy of a dict before running operations like .update(), and prevents
    errors on the original object by destroying the copy if an error is encountered, only
    overwriting the original if no errors occur.

    Params:
        original (dict): The original Python `dict`. A copy will be made during any operations, and will only overwrite
            the original if the operation succeeds.

    Usage:

    ``` py linenums="1"
        ex_dict = {"example": "value"}

        ## Protects from a ZeroDivision error
        with DictProtect(ex_dict) as copy:
            copy["example"] = 1 / 0

        print(f'Dict: {ex_dict}')
    ```
    """

    def __init__(self, original: dict) -> None:  # noqa: D107
        ## Call immediately after with DictProtect() as copy.
        if not isinstance(original, dict):
            raise TypeError(
                f"Invalid type for protected dict: ({type(original)}). Must be of type dict."
            )

        ## Set class value to original dict
        self.original = original

    def __enter__(self) -> dict:  # noqa: D105
        ## Call after initializing DictProtect instance.
        ## Create a copy of the dict to work on
        self.clone: dict = self.original.copy()

        return self.clone

    def __exit__(self, exc_type, exc_value, exc_traceback) -> bool:  # noqa: D105
        ## Call if DictProtect context manager encounters an error.
        ## No exception encountered, update original
        #  list and return
        if exc_type is None:
            self.original.update(self.clone)
        if exc_traceback:
            log.error(exc_traceback)

        ## Error encountered, print details
        else:
            ## https://docs.python.org/3/library/inspect.html?highlight=currentframe
            frame = inspect.currentframe()
            ## Full path to error file
            file_name = frame.f_code.co_filename
            ## Line number where error occurred.
            file_no = frame.f_lineno

            ## Build error details dict
            err = {
                "success": False,
                "detail": {
                    "module": file_name,
                    "line": file_no,
                    "exception_type": exc_type,
                    "exception_text": exc_value,
                },
            }

            ## Return error, exit returning original list
            log.error(
                f"Error encountered running dict operation on protected dict. Details: \n{err}"
            )

        return True
