"""A collection of context managers I use. Contains managers for database operations, function benchmarks,
and classes that aid in updating `dict`s and `list`s by creating a working copy that only overwrites the original
if the operation succeeds.
"""

from __future__ import annotations

from .benchmarks import async_benchmark, benchmark
from .database_managers.sqlite_managers import SQLiteConnManager
from .object_managers.protect import DictProtect, ListProtect
