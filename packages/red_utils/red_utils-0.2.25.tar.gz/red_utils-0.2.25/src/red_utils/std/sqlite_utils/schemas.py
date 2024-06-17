from __future__ import annotations

import logging

log = logging.getLogger("red_utils.std.sqlite_utils.schemas")

from dataclasses import dataclass, field
from pathlib import Path
import sqlite3

from red_utils.core import DB_DIR

@dataclass
class SQLiteDB:
    """Define a simple SQLite database path.

    Use this object's `.create_empty_db()` function to attempt to create a database at the object's `.db_path` property
    (this is a calculated property, available once the class is initialized).

    Params:
        name (str): The name of the database file
        ext (str): The file extension to use (`.db`, `.sqlite`, etc)
        location (str): Path where database file will be created. Database file will be created at `self.location`/`self.name` + `self.ext`

    Returns:
        (SQLiteDB): An initialized `SQLiteDB` object

    """

    name: str = field(default="demo")
    ext: str = field(default=".sqlite")
    location: str = field(default=DB_DIR)

    @property
    def filename(self) -> str:
        _filename: str = f"{self.name}{self.ext}"

        return _filename

    @property
    def db_path(self) -> str:
        _path: str = f"{self.location}/{self.filename}"

        return _path

    @property
    def exists(self) -> bool:
        if Path(self.db_path).exists():
            return True
        else:
            return False

    @property
    def stat_str(self) -> str:
        _str: str = (
            f"[{self.filename}] | {'Exists' if self.exists else 'Does not exist'} @ {self.db_path}/"
        )

        return _str

    def create_empty_db(self) -> bool:
        if not self.exists:
            try:
                connection = sqlite3.Connection = sqlite3.connect(self.db_path)
                log.debug(f"Initializing empty database file at: {self.db_path}")

                connection.close()

                return True
            except Exception as exc:
                msg = Exception(
                    f"Unhandled exception initializing an empty SQLite database at {self.db_path}. Details: {exc}"
                )
                log.error(msg)

                return False
        else:
            return True

    def __post_init__(self) -> None:  # noqa: D105
        if not self.ext.startswith("."):
            self.ext = f".{self.ext}"

        if not Path(self.db_path).exists():
            Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)
