"""Context manager utilities for interacting with SQLite databases, using
the stdlib sqlite3 library.

The `SQLiteConnManager` class facilitates clean & safe transactions to the database by
trying operations before committing.
"""

from __future__ import annotations

import logging

log = logging.getLogger("red_utils.std.context_managers.database_managers")

from pathlib import Path
import sqlite3
from typing import Union

class SQLiteConnManager:
    """Handle interactions with a SQLite database.

    Uses built-in functions to query a database, execute SQL statements,
    and gracefully open/close the DB using context managers.

    Params:
        path (str | Path): A path to a SQLite database file to work on.

    Usage:
    Provide a path string to the SQLite database:
    ``` py linenums="1"
    sqlite_connection = SQLiteConnManager(path="/path/to/db.sqlite")
    ```

    Call sqlite3 functions, i.e. `.get_tables()`:
    ``` py linenums="1"
    tables = sqlite_conn.get_tables()
    ```
    """

    def __init__(self, path: Path):  # noqa: D107
        ## Initialize SQLite connection manager.
        if isinstance(path, str):
            path: Path = Path(path)

        self.path = path

    def __enter__(self):  # noqa: D105
        ## Executed automatically when class is used as a context handler, like `with SQLiteConnManager() as conn: ...`
        if not self.path.exists():
            log.error(
                FileNotFoundError(f"Database does not exist at path: {self.path}.")
            )
            with sqlite3.connect(self.path):
                pass

        try:
            self.connection: sqlite3.Connection = sqlite3.connect(self.path)
            self.connection.row_factory = sqlite3.Row
            self.cursor: sqlite3.Cursor = self.connection.cursor()

            ## Return self, a configured SQLite client
            return self
        except FileNotFoundError as fnf:
            msg = FileNotFoundError(
                f"Database not found at path: {self.path}. Details: {fnf}"
            )
            log.error(msg)

            raise fnf
        except PermissionError as perm:
            msg = PermissionError(
                f"Unable to open database at path: {self.path}. Details: {perm}"
            )
            log.error(msg)

            raise perm
        except sqlite3.Error as sqlite_exc:
            msg = sqlite3.Error(f"SQLite3 error encountered. Details: {sqlite_exc}")
            log.error(msg)

            raise sqlite_exc
        except Exception as exc:
            msg = Exception(
                f"Unhandled exception connecting to database. Details: ({exc.__class__}) {exc}"
            )
            log.error(msg)

            raise exc

    def __exit__(self, exc_type, exc_val, exc_traceback):  # noqa: D105
        if exc_val:
            log.error(f"({exc_type}): {exc_val}")
        if exc_traceback:
            log.error(exc_traceback)

        ## Executed automatically when `with SQLiteConnManager()` exits. Executes on success or failure.
        self.connection.close()

    def get_cols(self, table: str = None) -> list[str]:
        """Return list of column names from a given table.

        Params:
            table (str): Name of the table in the SQLite database

        Returns:
            (list[str]): List of column names found in table

        """
        cols: list[str] = []
        stmt: str = f"SELECT * FROM {table}"

        try:
            with SQLiteConnManager(self.path) as conn:
                cursor = conn.cursor
                res = cursor.execute(stmt).fetchone()

                for col in res.keys():
                    cols.append(col)

                return cols

        except Exception as exc:
            msg = Exception(f"Unhandled exception executing SQL. Details: {exc}")
            log.error(msg)

            raise exc

    def get_tables(self) -> list[str]:
        """Get all table names from a SQLite databse.

        Returns:
            (list[str]): List of table names found in SQLite database.

        """
        get_tbls_stmt: str = "SELECT name FROM sqlite_master WHERE type='table';"
        tables: list[str] = []

        try:
            with SQLiteConnManager(self.path) as conn:
                cursor = conn.cursor
                res = cursor.execute(get_tbls_stmt).fetchall()

                for row in res:
                    tables.append(row["name"])

                return tables

        except Exception as exc:
            msg = Exception(f"Unhandled exception getting tables. Details: {exc}")
            log.error(msg)

            raise exc

    def run_sqlite_stmt(self, stmt: str = None) -> list[sqlite3.Row]:
        """Execute a SQL statement.

        Params:
            stmt (str): The SQL statement to execute against a SQLite database

        Returns:
            (list[sqlite3.Row]): The results from executing the query

        """
        assert stmt, "Must pass a SQL statement"
        assert isinstance(stmt, str), "Statement must be a Python str"

        try:
            with SQLiteConnManager(self.path) as conn:
                cursor = conn.cursor
                res = cursor.execute(stmt).fetchall()

            return res
        except Exception as exc:
            msg = Exception(
                f"Unhandled exception running SQL statement. Details: {exc}"
            )
            log.error(msg)

            raise exc
