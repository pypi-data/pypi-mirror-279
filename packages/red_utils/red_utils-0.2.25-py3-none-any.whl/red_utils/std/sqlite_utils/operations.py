"""Methods for interacting with a SQLite database."""

from __future__ import annotations

import logging

log = logging.getLogger("red_log.std.sqlite_utils")

from pathlib import Path
from typing import Union

from .schemas import SQLiteDB

def init_sqlite_db(db_definition: SQLiteDB = None) -> bool:
    """Initialize an empty SQLite database.

    Params:
        db_definition (SQLiteDB): An initialized SQLiteDB object defining the SQLite database to create.

    Returns:
        (bool): `True` if SQLite database successfully initialized
        (bool): `False` if SQLite database initialization unsuccessful

    Raises:
        Exception: When initializing empty SQLite database fails

    """
    if db_definition is None:
        raise ValueError("Missing SQLiteDB object.")

    if db_definition.exists:
        log.warning(f"Database already exists at {db_definition.db_path}")
        return False

    try:
        db_definition.create_empty_db()

        return True

    except Exception as exc:
        msg = Exception(
            f"Unhandled exception initializing empty SQLite database. Details: {exc}"
        )
        log.error(msg)

        return False


def get_demo_db() -> SQLiteDB:
    """Return an initialized SQLiteDB object with default settings.

    Returns:
        (SQLiteDB): An initialized `SQLiteDB` instance. A SQLite database file will also be created at the path: `.db/demo.db`

    Raises:
        Exception: When SQLite database initialization is unsuccessful

    """
    try:
        _db: SQLiteDB = SQLiteDB()
        return _db
    except Exception as exc:
        msg = Exception(
            f"Unhandled exception initializing default database. Details: {exc}"
        )
        log.error(msg)

        raise exc


def get_sqlite_db(name: str = None, location: Union[str, Path] = None) -> SQLiteDB:
    """Initialize a SQLiteDB object.

    This is the same as simply instantiating a SQLiteDB object, like:

    ``` py linenums="1"
    example_db: SQLiteDB = SQLiteDB(name=..., location=...)
    ```

    Params:
        name (str): The name of the SQLite database. This will be used for the filename.
            location (str|Path): The directory location to save the database. Note that Path values will be converted to string, then
            back to Path, so it is best to just pass the location as a string.

    Returns:
        (SQLiteDB): An initialized `SQLiteDB` object

    Raises:
        ValueError: When input value validation fails
        Exception: When SQLite database initialization fails

    """
    if name is None:
        raise ValueError("Missing database name")
    if location is None:
        raise ValueError("Missing output path location for database")
    if isinstance(location, Path):
        location: str = str(location)

    try:
        _db: SQLiteDB = SQLiteDB(name=name, location=location)
        return _db
    except Exception as exc:
        raise Exception(f"Unhandled exception creating SQLite database. Details: {exc}")


if __name__ == "__main__":
    demo_db: SQLiteDB = SQLiteDB()
    log.info(demo_db.stat_str)

    init_sqlite_db(demo_db)
