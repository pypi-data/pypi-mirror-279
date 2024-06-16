"""SQLAlchemy common database code.

Contains SQLAlchemy setup code, engine, and session(s). Uses `dataclasses` to define
database connection, and builds a default `Engine` & `Session`. The use of `dataclasses` is
to minimize depdencies for this common SQLAlchemy code so it can be easily re-used in
other projects utilizing SQLAlchemy for database operations.

The default `Engine` and `Session` are customizable using the `get_engine()` and `get_session()`
functions. These functions can be imported & called from another app, with customized
values to control engine & session behavior.

Currently supported databases:
    - [x] SQLite
    - [x] Postgres
    - [ ] MySQL
    - [x] MSSQL
    - [ ] Azure Cosmos
    
Be sure to import the `Base` object from this script and run `Base.metadata.create_all(bind=engine)`
as early as possible. For example, import the `Base` object from this script into a `main.py` or equivalent entrypoint,
create/import an `Engine`, and immediately run the metadata create function.
"""

from __future__ import annotations

from importlib.util import find_spec

from red_utils.exc import CustomModuleNotFoundError, MissingDependencyException

if find_spec("sqlalchemy"):
    from . import base, connection_models, constants, repository, utils
    from ._depends import get_db

    ## Import SQLAlchemy dependencies
    from .base import Base

    ## Import SQLAlchemy connection classes
    from .connection_models import (
        saConnectionGeneric,
        saMSSQLConnection,
        saMySQLConnection,
        saPGConnection,
        saSQLiteConnection,
    )

    ## Import constants
    from .constants import valid_db_types
    from .custom_types import CompatibleUUID
    from .db_config import DBSettings
    from .mixins import TableNameMixin, TimestampMixin
    from .repository import RepositoryBase

    ## Import custom SQLAlchemy utils
    from .utils import (
        create_base_metadata,
        debug_metadata_obj,
        generate_metadata,
        get_engine,
        get_session_pool,
        validate_db_type,
    )
