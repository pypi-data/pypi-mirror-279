"""Utilities & classes for interacting with the builtin `sqlite` module.
"""

from __future__ import annotations

import sys

sys.path.append(".")

from .operations import get_demo_db, get_sqlite_db, init_sqlite_db
from .schemas import SQLiteDB
