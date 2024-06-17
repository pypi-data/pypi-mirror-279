from __future__ import annotations

import logging

log = logging.getLogger("red_utils.ext.sqlalchemy_utils.utils")

from typing import Any, Optional, Union

from .connection_models import (
    saConnectionGeneric,
    saMSSQLConnection,
    saPGConnection,
    saSQLiteConnection,
)
from .constants import valid_db_types

import sqlalchemy as sa
from sqlalchemy.exc import DBAPIError, OperationalError
import sqlalchemy.orm as so
from sqlalchemy.schema import CreateTable

def debug_metadata_obj(metadata_obj: sa.MetaData = None) -> None:
    """Debug-print a SQLAlchemy MetaData object.

    Loop over tables and print names.

    Params:
        metadata_obj (sqlalchemy.MetaData): A SQLAlchemy `MetaData` object to debug
    """
    if not metadata_obj:
        raise ValueError("Missing a SQLAlchemy metadata object.")

    if not isinstance(metadata_obj, sa.MetaData):
        raise ValueError(
            f"Expected a MetaData obj, not object of type '{type(metadata_obj).__name__}'"
        )

    for _table in metadata_obj.sorted_tables:
        print(f"Table name: {_table.name}")


## Ensure a supported database is used
def validate_db_type(in_str: str = None) -> bool:
    """Validate `db_type` string in functions that utilize `db_type`.

    Params:
        in_str (str): A `db_type` string to validate

    Returns:
        (bool): `True` if `in_str` is valid

    Raises:
        ValueError: If the `in_str` is not valid

    """
    if not in_str:
        raise ValueError("Missing input string to validate")

    if in_str not in valid_db_types:
        return False

    return True


def generate_metadata(
    metadata_obj: sa.MetaData = None, engine: sa.Engine = None
) -> None:
    """Create SQLAlchemy table metadata.

    Accept a SQLalchemy MetaData object, run .create_all(engine) to create
    table metadata.

    Params:
        metadata_obj (sqlalchemy.MetaData): A SQLAlchemy `MetaData` object to use for generating in the database
        engine (sqlalchemy.Engine): The SQLAlchemy `Engine` to use for the database connection

    Raises:
        ValueError: When input values are invalid
        OperationalError: When SQLAlchemy runs into an error with the database, usually starting
            on the database (not in SQLAlchemy)
        DBAPIERROR: When SQLAlchemy runs into an issue, generally in the way you've coded a SQLAlchemy
            statement or operation
        Exception: When an uncaught/unhandled exception occurs

    """
    if not metadata_obj:
        raise ValueError("Missing a SQLAlchemy MetaData object.")

    if not isinstance(metadata_obj, sa.MetaData):
        raise ValueError(
            f"Expected a MetaData obj, not object of type '{type(metadata_obj).__name__}'"
        )

    if not engine:
        raise ValueError("Missing a SQLAlchemy engine object.")

    if not isinstance(engine, sa.Engine):
        raise ValueError(
            f"Expected a SQLAlchemy engine obj, not object of type '{type(engine).__name__}"
        )

    try:
        metadata_obj.create_all(engine)

        return True
    except OperationalError as op_exc:
        raise op_exc
    except DBAPIError as dbapi_exc:
        raise dbapi_exc
    except Exception as exc:
        raise Exception(f"Unhandled exception creating Base metadata. Details: {exc}")


def create_base_metadata(
    base_obj: so.DeclarativeBase = None, engine: sa.Engine = None
) -> bool:
    """Create `Base` object's metadata.

    Description:
        Import this function early in your app/script (i.e. `main.py`) and run as soon as
        possible, i.e. after imports.

        This function accepts a SQLAlchemy `DeclarativeBase` object, and creates the table
        metadata from that object using the `Engine` passed.

        This function will only ever return `True` if successful. It does not return `False`,
        as an `Exception` is raised if metadata creation fails and the program is halted.

    Params:
        base_obj (sqlalchemy.DeclarativeBase): A SQLAlchemy `DeclarativeBase` object to extract metadata from
        engine (sqlalchemy.Engine): The `Engine` to use for the database connection.

    Returns:
        (bool): `True` if creating `Base` metadata is successful

    Raises:
        ValueError: When input values are invalid
        OperationalError: When SQLAlchemy runs into an error with the database, usually starting
            on the database (not in SQLAlchemy)
        DBAPIERROR: When SQLAlchemy runs into an issue, generally in the way you've coded a SQLAlchemy
            statement or operation
        Exception: When an uncaught/unhandled exception occurs

    """
    try:
        base_obj.metadata.create_all(bind=engine)

        return True
    except OperationalError as op_exc:
        raise op_exc
    except DBAPIError as dbapi_exc:
        raise dbapi_exc
    except Exception as exc:
        raise Exception(f"Unhandled exception creating Base metadata. Details: {exc}")


def get_engine(
    connection: Union[saSQLiteConnection, saPGConnection, str] = None,
    db_type: str = "sqlite",
    echo: bool = False,
    pool_pre_ping: bool = False,
) -> sa.Engine:
    """Return a SQLAlchemy Engine object.

    [SQLAlchemy docs: Engine](https://docs.sqlalchemy.org/en/20/tutorial/engine.html)

    To use a database other than SQLite, i.e. Postgres or MySQL, pass
    the lowercase string name of the database.

    Currently supported databases:
        - [x] SQLite
        - [x] Postgres
        - [ ] MySQL
        - [x] MSSQL
        - [ ] Azure Cosmos

    Params:
        connection (saSQLiteConnection, saPGConnection): Instantiated instance of a custom database connection class
        db_type (str): The string name (lowercase) of a database type
        echo (bool): If `True`, the SQL the `Engine` runs will be echoed to the CLI
        pool_pre_ping (bool): Test connection pool before starting operations

    Returns:
        (sqlalchemy.Engine): An initialized SQLAlchemy `Engine` object

    """
    if not connection:
        raise ValueError("Missing connection object/string.")

    if isinstance(connection, str):
        if db_type == "sqlite":
            connection: saSQLiteConnection = saSQLiteConnection(database=connection)

    ## Validate db_type input
    if db_type:
        _valid: bool = validate_db_type(db_type)

        if not _valid:
            raise ValueError(
                f"Invalid db_type: {db_type}. Must be one of: {valid_db_types}"
            )

    else:
        ## Default to sqlite if no db_type is passed
        db_type = "sqlite"

    if db_type == "sqlite":
        ## Ensure path to database file exists
        connection.ensure_path()

    if db_type == "postgres":
        pass

    if db_type == "mssql":
        pass

    try:
        engine = sa.create_engine(
            connection.connection_string, echo=echo, pool_pre_ping=pool_pre_ping
        )

        return engine

    except OperationalError as op_exc:
        raise OperationalError(
            f"SQLAlchemy OperationalError exception occurred connecting to database {connection.database}. Details: {op_exc}"
        )

    except Exception as exc:
        raise Exception(f"Unhandled exception creating database engine. Details: {exc}")


def get_session_pool(
    engine: sa.Engine = None,
    autoflush: bool = False,
    expire_on_commit: bool = False,
    class_=so.Session,
) -> so.sessionmaker[so.Session]:
    """Define a factory for creating SQLAlchemy sessions.

    Returns a `sqlalchemy.orm.sessionmaker` `Session` instance. Import this
    function in scripts that interact with the database, and create a
    `SessionLocal` object with `SessionLocal = get_session(**args)`

    Params:
        engine (sqlalchemy.Engine): A SQLAlchemy `Engine` object to use for connections
        autoflush (bool): Automatically run `flush` operation on commits
        expire_on_commit (bool): If `True`, connection expires once it's closed
        class_: You can specify a class which should be returned instead of `sqlalchemy.orm.Session`.
            [SQLAlchemy: sessionmaker class_ docs](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.params.class_)

    Returns:
        (sessionmaker[Session]): An initialized `Session` instance

    """
    try:
        session_pool: so.sessionmaker[so.Session] = so.sessionmaker(
            bind=engine,
            autoflush=autoflush,
            expire_on_commit=expire_on_commit,
            class_=class_,
        )

        return session_pool

    except Exception as exc:
        raise Exception(
            f"Unhandled exception creating a sessionmaker Session. Details: {exc}"
        )
