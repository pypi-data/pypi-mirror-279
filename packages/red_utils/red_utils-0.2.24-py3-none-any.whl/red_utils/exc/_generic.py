from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .base import CustomExceptionBase

@dataclass
class CustomException(CustomExceptionBase):
    """A generic Exception.

    Description: This object can store arbitrary types in one of 2 extra fields:

    - errors
    - extra

    `errors` is meant to store an error/a list of errors.
    `extra` is meant to store any non-message, non-error data with the exception. This could be a class
    object, a dict, or some other form of arbitrary data.

    Params:
        msg (str): A message to display with the exception.
        errors (Any): Property to store arbitrary data. Meant to be used for errors associated with the exception.
        extra (Any): Property to store arbitrary data.
            Data stored in this property can be a Python object (i.e. a class
            instance, dict, str, or other), a list of objects/strings, etc.

    Usage:
        ``` py
        try:
            ...
        except CustomException as exc:
            raise CustomException(msg="Custom exception occurred", errors=exc)
        ```
    """

    errors: Any | None = field(default=None)
    extra: Any | None = field(default=None)

    def __repr__(self):
        repr_str: str = f"{self.msg!r}"

        if self.errors is not None:
            repr_str: str = f"{repr_str}\nErrors: {self.errors!r}"
        if self.extra is not None:
            repr_str: str = f"{repr_str}\nExtra: {self.extra!r}"

        return repr_str

    def __str__(self):
        return repr(self)
