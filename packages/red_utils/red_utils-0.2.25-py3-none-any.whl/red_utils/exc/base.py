from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Union

@dataclass
class CustomExceptionBase(BaseException):
    """Base class for custom exceptions to inherit from.

    This class itself inherits from Python's Exception class.

    Params:
        msg (str): A message to display with the exception

    Usage:
        ``` py linenums="1"

        raise CustomExceptionBase(msg="This is a custom exception")
        ```
    """

    msg: str = field(default="Custom exception called")
    # errors: Any | None = field(default=None)
    # extra: Any | None = field(default=None)

    def __repr__(self):
        repr_str: str = f"{self.msg!r}"

        return repr_str

    def __str__(self):
        return repr(self)
