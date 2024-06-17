"""Utilities for `pydantic`"""

from __future__ import annotations

from importlib.util import find_spec

if find_spec("pydantic"):
    from . import parsers
    from .parsers import parse_pydantic_schema
