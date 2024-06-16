"""Core utilities for dataclasses.

Mostly used in `red_utils.std`, but can be imported into
any Python script that declares `dataclasses.dataclass` classes.
"""

from __future__ import annotations

from . import mixins
from .mixins import DictMixin
