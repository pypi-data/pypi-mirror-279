from __future__ import annotations

from typing import Union

from httpx import AsyncClient, Client
from httpx._types import HeaderTypes

valid_methods: list[str] = [
    "CONNECT",
    "DELETE",
    "GET",
    "HEAD",
    "OPTIONS",
    "PATCH",
    "POST",
    "PUT",
    "TRACE",
]


def validate_method(method: str = None) -> str:
    """Validate an HTTPX request method.

    Params:
    - method (str): The method to validate.
    """
    if method is None:
        raise ValueError("Missing a method to validate")
    if not isinstance(method, str):
        try:
            method: str = str(method).upper()
        except Exception as exc:
            raise Exception(
                f"Unable to coerce method value to string: ({type(method)}) - {method}. Details: {exc}"
            )
    else:
        method: str = method.upper()

    if method not in valid_methods:
        raise ValueError(f"Invalid method: {method}. Must be one of {valid_methods}")

    return method


def validate_client(
    client: Union[Client, AsyncClient] = None
) -> Union[Client, AsyncClient]:
    """Validate HTTPX Client/AsyncClient object."""
    if not client:
        raise ValueError("Missing client to evaluate")

    if not isinstance(client, Client) and not isinstance(client, AsyncClient):
        raise TypeError(
            f"Invalid type for client: {type(client)}. Must be one of [{Client}, {AsyncClient}]"
        )

    return client


def validate_headers(
    headers: Union[HeaderTypes, dict[str, str]] = None
) -> dict[str, str]:
    if not headers:
        # raise ValueError("Missing headers to evaluate")
        return

    if not isinstance(headers, dict):
        raise TypeError(
            f"Invalid type for headers: ({type(headers)}). Must be dict[str, str]"
        )

    return headers
