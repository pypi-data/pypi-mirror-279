from __future__ import annotations

import logging
from pathlib import Path
import sqlite3
import typing as t

log = logging.getLogger("weatherbot.request_client.cache_storages")

import hishel

def get_hishel_file_storage(
    cache_dir: t.Union[str, Path] = None,
    ttl: t.Union[int, float] | None = None,
    check_ttl_every: t.Union[int, float] = 60,
) -> hishel.FileStorage:
    cache_dir: Path = Path(f"{cache_dir}")

    try:
        _storage: hishel.FileStorage = hishel.FileStorage(
            base_path=cache_dir, ttl=ttl, check_ttl_every=check_ttl_every
        )

        return _storage
    except Exception as exc:
        msg = Exception(
            f"Unhandled exception initializing hishel.FileStorage object. Details: {exc}"
        )
        log.error(msg)

        raise exc


def get_hishel_inmemory_storage(
    ttl: t.Union[int, float] | None = None, capacity: int = 128
) -> hishel.InMemoryStorage:
    try:
        _storage: hishel.InMemoryStorage = hishel.InMemoryStorage(
            ttl=ttl, capacity=capacity
        )

        return _storage
    except Exception as exc:
        msg = Exception(
            f"Unhandled exception initializing hishel.InMemoryStorage. Details: {exc}"
        )
        log.error(msg)

        raise exc


def get_hishel_sqlite_storage(
    sqlite_db_filepath: t.Union[str, Path] = None,
    sqlite_db_timeout: int = 5,
    sqlite_db_check_same_thread: bool = True,
    ttl: t.Union[int, float] | None = None,
) -> hishel.SQLiteStorage:
    sqlite_db_filepath: Path = Path(f"{sqlite_db_filepath}")

    try:
        sqlite_conn = sqlite3.connect(
            f"{sqlite_db_filepath}",
            timeout=sqlite_db_timeout,
            check_same_thread=sqlite_db_check_same_thread,
        )
    except Exception as exc:
        msg = Exception(
            f"Unhandled exception getting SQLite3 connection. Details: {exc}"
        )
        log.error(msg)

        raise exc

    try:
        _storage: hishel.SQLiteStorage = hishel.SQLiteStorage(
            connection=sqlite_conn, ttl=ttl
        )

        return _storage
    except Exception as exc:
        msg = Exception(
            f"Unhandled exception initializing hishel.SQLiteStorage object. Details: {exc}"
        )
        log.error(msg)

        raise exc


def get_hishel_redis_storage() -> hishel.RedisStorage:
    raise NotImplementedError()

    _storage: hishel.RedisStorage = hishel.RedisStorage()
