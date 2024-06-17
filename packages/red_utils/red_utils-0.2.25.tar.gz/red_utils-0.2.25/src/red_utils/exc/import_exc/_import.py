from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from red_utils.exc import CustomException

class CustomModuleNotFoundError(ModuleNotFoundError):
    def __init__(
        self, msg: str = None, missing_dependencies: list[str] | None = None
    ) -> None:
        self.msg: str | None = msg
        self.missing_dependencies: list[str] | None = missing_dependencies

    def __repr__(self) -> str:
        return f"{self.msg!r}: {self.missing_dependencies!r}"


@dataclass
class MissingDependencyException(CustomException):
    """Exception to raise when an import is called but a dependency is missing.

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
    missing_dependencies: list[str] | None = field(default_factory=list())

    def __repr__(self):
        repr_str: str = f"{self.msg!r}"

        if self.errors is not None:
            repr_str: str = f"{repr_str}\nErrors: {self.errors!r}"
        if self.extra is not None:
            repr_str: str = f"{repr_str}\nExtra: {self.extra!r}"

        return repr_str

    def __str__(self):
        return repr(self)

    @property
    def exc_msg(self):
        msg = CustomModuleNotFoundError(
            msg=self.msg, missing_dependencies=self.missing_dependencies
        )

        return msg
