"""Extras for diskcache_utils.

Separates some functions/classes from the main diskcache_utils to shorten
length of individual scripts.
"""

from __future__ import annotations

import logging

log = logging.getLogger("red_utils.ext.diskcache_utils")

from pathlib import Path
from typing import Optional, Type, Union

from red_utils.core.constants import CACHE_DIR

from .validators import (
    validate_cache,
    validate_expire,
    validate_key,
    validate_read,
    validate_retry,
    validate_tag,
    validate_tags,
    validate_val,
)

import diskcache
from diskcache import Cache


def convert_to_seconds(amount: int = None, unit: str = None) -> int:
    """Convert an amount of time to seconds.

    Params:
        amount (int): Amount of time
        unit (str): The starting unit of time to convert to seconds.
            Options: ["seconds", "hours", "minutes", "days", "weeks"]

    Returns:
        (int): `amount` of time converted to seconds representing the `unit` of time passed

    """
    ## Allowed strings for conversion
    valid_time_units: list[int] = ["seconds", "hours", "minutes", "days", "weeks"]

    assert unit is not None, ValueError(
        f"Missing unit. Must be one of {valid_time_units}"
    )

    assert isinstance(unit, str), TypeError(
        f"Invalid type for unit: {type(unit)}. Must be str"
    )

    assert unit in valid_time_units, TypeError(
        f"Invalid unit: {unit}. Must be one of {valid_time_units}"
    )

    amount is not None, ValueError("Missing amount of unit, i.e. 3 days")

    assert isinstance(amount, int), TypeError(
        f"Invalid type for amount: ({type(amount)}). Must be of type int"
    )

    match unit:
        case "weeks":
            _amount: int = amount * 7 * 24 * 60 * 60
        case "days":
            _amount: int = amount * 24 * 60 * 60
        case "hours":
            _amount: int = amount * 60 * 60
        case "minutes":
            _amount: int = amount * 60
        case "seconds":
            _amount: int = amount
        case _:
            raise ValueError(f"Invalid input for unit: {unit}")

    return _amount


def new_cache(
    cache_dir: str = CACHE_DIR,
    cache_conf: dict = None,
    index: bool = True,
) -> diskcache.core.Cache:
    """Prepare and return a diskcache.Cache object.

    Params:
        cache_dir (str): Directory path where cache will be created
        cache_conf (dict): A Python `dict` with cache configuration options
        index (bool): Whether or not to create an index for the cache

    Returns:
        (diskcache.core.Cache): An initialized `diskcache.Cache` object

    """
    assert cache_dir is not None, ValueError("Missing cache directory")

    assert isinstance(cache_dir, Union[str, Path]), TypeError(
        f"cache_dir must be of type str or Path, not {type(cache_dir)}"
    )

    assert cache_conf is not None, ValueError(f"Missing cache")

    assert isinstance(cache_conf, dict), TypeError(
        f"Invalid type for [cache_conf]: ({type(cache_conf)}). Must be of type dict."
    )

    try:
        # _cache: diskcache.core.Cache = Cache(directory=cache_dir)
        _cache: diskcache.core.Cache = Cache(**cache_conf)

        if index:
            manage_cache_tag_index(cache=_cache)

        return _cache

    except Exception as exc:
        msg = Exception(f"Unhandled exception creating cache. Details: {exc}")
        log.error(msg)

        raise exc


def clear_cache(cache: Cache = None) -> bool:
    """Clear all items from the cache.

    Params:
        cache (diskcache.Cache): The target cache to clear

    Returns:
        (bool): `True` if cache cleared successfully
        (bool): `False` if cache not cleared successfully

    """
    validate_cache(cache)

    try:
        with cache as ref:
            ref.clear()

            return True

    except Exception as exc:
        msg = Exception(
            f"Unhandled exception clearing cache at {cache.directory}. Details: {exc}"
        )
        log.error(msg)

        raise exc


def check_cache_key_exists(cache: diskcache.core.Cache = None, key: str = None) -> bool:
    """Check if a key exists in a cache.

    Params:
        cache (diskcache.Cache): A `diskcache.Cache` instance to check
        key (str): The key name to search the `cache` for

    Returns:
        (bool): `True` if the key exists
        (bool): `False` if the key does not exist

    """
    ## Key validation
    validate_key(key=key)
    validate_cache(cache=cache)

    ## Check if key exists in cache
    if key in cache:
        return True
    else:
        return False


def manage_cache_tag_index(cache: Cache = None, operation: str = "create") -> None:
    """Create or delete a cache's tag index.

    Params:
        cache (diskcache.Cache): A `diskcache.Cache` instance to work on
        operation (str): The operation (create/delete) to perform on the tag index
    """
    valid_operations: list[str] = ["create", "delete"]

    validate_cache(cache=cache)

    if not operation:
        raise Exception(f"Operation cannot be None.")

    try:
        match operation:
            case "create":
                if cache.tag_index == 0:
                    cache.create_tag_index()
                else:
                    pass

            case "delete":
                if cache.tag_index == 1:
                    cache.drop_tag_index()
                else:
                    pass

            case _:
                raise ValueError(
                    f"Invalid operation: {operation}. Must be one of {valid_operations}"
                )

    except Exception as exc:
        msg = Exception(f"Unhandled exception configuring tag_index. Details: {exc}")
        log.error(msg)

        raise exc


def set_val(
    cache: Cache = None,
    key: Union[str, int, tuple, frozenset] = None,
    val: Union[str, bytes, float, int, list, dict] = None,
    expire: int = None,
    read: bool = False,
    tag: str = None,
    retry: bool = False,
) -> None:
    """Set a key value pair in the cache.

    Params:
        cache (diskcache.Cache): A `diskcache.Cache` object to work on
        key (str): The key to store the value under in the cache
        val (str): The value to store in the cache
        expire (int): Time (in seconds) before value expires
        read (bool): If `True`, read value as a file-like object
        tag (str): Applies a tag to the cached value
        retry (bool): If `True`, retry setting cache key if first attempt fails
    """
    validate_key(key)
    validate_val(val)
    validate_expire(expire, none_ok=True)
    validate_read(read, none_ok=True)
    validate_tag(tag=tag, none_ok=True)
    validate_retry(retry=retry, none_ok=True)
    validate_cache(cache=cache)

    try:
        with cache as ref:
            ref.set(key=key, value=val, expire=expire, read=read, tag=tag, retry=retry)

    except Exception as exc:
        msg = Exception(
            f"Unhandled exception setting key/value pair for key: [{key}]. Details: {exc}"
        )
        log.error(msg)

        raise exc


def set_expire(
    cache: Cache = None, key: str = None, expire: int = None
) -> Union[dict[str, str], None]:
    """Set/change a cache key's expiration time.

    Params:
        cache (diskcache.Cache): A `diskcache.Cache` instance to work on
        key (str): The cache key name to set an expiration time on
        expire (int): Time (in seconds) before cache key expires
    """
    validate_key(key)
    validate_cache(cache)
    validate_expire(expire)

    if not check_cache_key_exists(key=key, cache=cache):
        return {
            "warning": f"Cache item with key [{key}] does not exist in cache at {cache.directory}/"
        }

    try:
        with cache as ref:
            ref.touch(key, expire=expire)

    except Exception as exc:
        msg = Exception(
            f"Unhandled exception setting expiration of {expire} on key [{key}] in cache at {cache.directory}/. Details: {exc}"
        )
        log.error(msg)

        raise exc


def get_val(cache: Cache = None, key: str = None, tags: list[str] = None):
    """Search for a key in a given cache.

    Params:
        cache (diskcache.Cache): A `diskcache.Cache` instance to work on
        key (str): A key name to retrieve from the cache
        tags: A list of tags to filter by

    Returns:
        (Any): The cached value
        (dict[str, str]): A structured dict with error details, if operation fails

    """
    validate_key(key)
    validate_cache(cache)
    validate_tags(tags)

    try:
        if check_cache_key_exists(key=key, cache=cache):
            try:
                with cache as ref:
                    _val = ref.get(key=key)

                    return _val

            except Exception as exc:
                msg = Exception(
                    f"Unhandled exception retrieving value of key [{key}]. Details: {exc}"
                )
                log.error(msg)

                raise exc

        else:
            return {
                "error": "Key not found in cache",
                "details": {"key": key, "cache_dir": cache.directory},
            }

    except Exception as exc:
        return {
            "error": "Error searching for key in cache",
            "details": {"exception": exc},
        }


def delete_val(
    cache: Cache = None, key: Union[str, int, tuple, frozenset] = None, tag: str = None
) -> tuple:
    """Delete a value from the cache.

    Params:
        cache (diskcache.Cache): A `diskcache.Cache` instance to work on
        key (str): The name of a key to delete
        tag (str): Tag to filter by
    """
    validate_key(key)
    validate_cache(cache)
    validate_tag(tag)

    try:
        with cache as ref:
            _delete = ref.pop(key=key, tag=tag)

            return _delete

    except Exception as exc:
        msg = Exception(
            f"Unhandled exception deleting key {key} from cache at {cache.directory}/. Details: {exc}"
        )
        log.error(msg)

        raise exc


def get_cache_size(cache: Cache = None) -> dict[str, int]:
    """Get the total size of a `diskcache.Cache` instance.

    Params:
        cache (diskcache.Cache): A `diskcache.Cache` object to get the size of

    Returns:
        (dict[str, int]): Details about the cache's size. Example:
            `{"unit": "bytes", "size": cache_size}`

    """
    validate_cache(cache=cache)

    try:
        cache_size: int = cache.volume()

    except Exception as exc:
        msg = Exception(f"Unhandled exception getting cache size. Details: {exc}")
        log.error(msg)

        raise exc

    return {"unit": "bytes", "size": cache_size}


def check_cache(cache: Cache = None):
    """Run healthcheck on cache.

    Params:
        cache (diskcache.Cache): A `diskcache.Cache` instance to work on
    """
    validate_cache(cache=cache)

    try:
        warnings = cache.check()

        return warnings

    except Exception as exc:
        msg = Exception(
            f"Unhandled exception checking cache for warnings. Details: {exc}"
        )
        log.error(msg)

        raise exc
