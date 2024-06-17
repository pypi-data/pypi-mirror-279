"""Dependencies for database.

Includes functions like `get_db()`, which is a context manager that yields a database session.
"""

from __future__ import annotations

import logging

log = logging.getLogger("red_utils.ext.sqlalchemy_utils.depends")

from contextlib import contextmanager
import typing as t

from .db_config import DBSettings

import sqlalchemy as sa
import sqlalchemy.orm as so

@contextmanager
def get_db(db_settings: DBSettings = None) -> t.Generator[so.Session, t.Any, None]:
    """Dependency to yield a SQLAlchemy Session pool.

    Usage:

    ```py title="get_db() dependency usage" linenums="1"

    from core.dependencies import get_db

    with get_db() as session:
        repo = someRepoClass(session)

        all = repo.get_all()
    ```
    """
    assert db_settings, ValueError("Missing DBSettings object.")

    SESSION_POOL: so.sessionmaker[so.Session] = db_settings.get_session_pool()

    db: so.Session = SESSION_POOL()

    try:
        yield db
    except Exception as exc:
        msg = Exception(
            f"Unhandled exception yielding database session. Details: {exc}"
        )
        log.error(msg)

        raise exc
    finally:
        db.close()
