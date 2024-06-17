from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, ByteString, Union

from .validators import valid_operations

@dataclass
class SerialFunctionResponseBase:
    success: bool = field(default=False)
    detail: Any | None = field(default=None)
    operation: str | None = field(default=None)

    def __post_init__(self):
        if self.operation is not None:
            if not isinstance(self.operation, str):
                raise TypeError(
                    f"Invalid type for operation: {type(self.operation)}. Must be of type str."
                )
            if self.operation not in valid_operations:
                raise ValueError(
                    f"Invalid operation: {self.operation}. Must be one of {valid_operations}"
                )


@dataclass
class SerialFunctionResponse(SerialFunctionResponseBase):
    """A `dataclass` for passing `msgpack` serialization responses.

    Params:
        success (bool): `True` if operation success, `False` if operation failure
        detail (Any): Append additional details to a response
        operation (str): The operation that produced this response.
            Can be serialize/deserialize, or serialize/deserialize file.
    """

    pass
