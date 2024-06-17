from __future__ import annotations

import logging

log = logging.getLogger("red_utils.core.dataclass_utils.mixins")

from dataclasses import dataclass
from typing import Generic, TypeVar

## Generic type for dataclass classes
T = TypeVar("T")


@dataclass
class DictMixin:
    """Mixin class to add "as_dict()" method to classes. Equivalent to .__dict__.

    Adds a `.as_dict()` method to classes that inherit from this mixin. For example,
    to add `.as_dict()` method to a parent class, where all children inherit the .as_dict()
    function, declare parent as:

    ``` py linenums="1"
    @dataclass
    class Parent(DictMixin):
        ...
    ```

    and call like:

    ``` py linenums="1"
    p = Parent()
    p_dict = p.as_dict()
    ```
    """

    def as_dict(self: Generic[T]):
        """Return dict representation of a dataclass instance.

        Description:
            Any class that inherits from `DictMixin` will automatically have a method `.as_dict()`.
                There are no extra params.

        Returns:
            (dict): A Python `dict` representation of a Python `dataclass` class.

        """
        try:
            return self.__dict__.copy()

        except Exception as exc:
            msg = Exception(
                f"Unhandled exception converting class instance to dict. Details: {exc}"
            )
            log.error(msg)

            raise exc
