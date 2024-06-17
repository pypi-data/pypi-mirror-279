import typing as t
import logging
from pathlib import Path
import json
import warnings

log = logging.getLogger("red_utils.ext.diskcache_utils.controllers")

from contextlib import AbstractContextManager

from red_utils.ext.diskcache_utils import validators

import diskcache


class DiskCacheController(AbstractContextManager):
    def __init__(
        self,
        cache_directory: t.Union[str, Path] | None = None,
        cache_timeout: int = 60,
        cache_disk: t.Type[diskcache.Disk] = diskcache.Disk,
        index: bool = True,
    ):
        self.cache_directory = Path(f"{cache_directory}")
        self.cache_timeout = cache_timeout
        self.cache_disk = cache_disk
        self.create_index = index

        self.cache = None

    def __enter__(self) -> t.Self:
        try:
            _cache: diskcache.Cache = diskcache.Cache(
                directory=self.cache_directory,
                timeout=self.cache_timeout,
                disk=self.cache_disk,
            )
        except Exception as exc:
            msg = Exception(
                f"Unhandled exception getting DiskCache Cache. Details: {exc}"
            )
            log.error(msg)

            raise exc

        self.cache = _cache

        if self.create_index:
            log.info("Creating cache index")
            try:
                self.manage_cache_tag_index("create")
            except Exception as exc:
                msg = Exception(
                    f"Unhandled exception creating cache index. Details: {exc}"
                )
                log.error(msg)

                raise exc

        return self

    def __exit__(self, exc_type, exc_val, traceback):
        if self.cache:
            self.cache.close()

        if exc_val:
            log.error(f"({exc_type}): {exc_val}")

        if traceback:
            raise traceback

    def manage_cache_tag_index(self, operation: str = "create") -> None:
        """Create or delete a cache index.

        Params:
            operation (str): The operation to perform on the cache's tag index.
                Options: ["create", "delete"]
        """
        valid_operations: list[str] = ["create", "delete"]

        validators.validate_cache(cache=self.cache)

        if not operation:
            raise Exception(f"Operation cannot be None.")

        try:
            match operation:
                case "create":
                    if self.cache.tag_index == 0:
                        self.cache.create_tag_index()
                    else:
                        pass

                case "delete":
                    if self.cache.tag_index == 1:
                        self.cache.drop_tag_index()
                    else:
                        pass

                case _:
                    raise ValueError(
                        f"Invalid operation: {operation}. Must be one of {valid_operations}"
                    )

        except Exception as exc:
            msg = Exception(
                f"Unhandled exception configuring tag_index. Details: {exc}"
            )
            log.error(msg)

            raise exc

    def clear(self) -> bool:
        """Clear the entire cache.

        Returns:
            (bool): `True` if clearing cache successful
            (bool): `False` if clearing the cache not successful

        """
        validators.validate_cache(self.cache)

        try:
            with self.cache as ref:
                ref.clear()

                return True

        except Exception as exc:
            msg = Exception(
                f"Unhandled exception clearing cache at {self.cache.directory}. Details: {exc}"
            )
            log.error(msg)

            raise exc

    def check_key_exists(self, key: t.Union[str, int, tuple, frozenset] = None) -> bool:
        """Check if a key exists in a cache.

        Params:
            key (str): The cache key to search for

        Returns:
            (bool): `True` if cache key found
            (bool): `False` if cache key not found

        """
        ## Key validation
        validators.validate_key(key=key)
        validators.validate_cache(cache=self.cache)

        ## Check if key exists in cache
        if key in self.cache:
            return True
        else:
            return False

    def set(
        self,
        key: t.Union[str, int, tuple, frozenset] = None,
        val: t.Union[str, bytes, float, int, list, dict] = None,
        expire: int = None,
        read: bool = False,
        tag: t.Union[str, int, float, bytes] = None,
        retry: bool = False,
    ) -> None:
        """Set a key value pair in the cache.

        Params:
            key (str): The key to store the value under in the cache
            val (str): The value to store in the cache
            expire (int): Time (in seconds) before value expires
            read (bool): If `True`, read value as a file-like object
            tag (str): Applies a tag to the cached value
            retry (bool): If `True`, retry setting cache key if first attempt fails
        """
        validators.validate_key(key)
        validators.validate_val(val)
        validators.validate_expire(expire, none_ok=True)
        validators.validate_read(read, none_ok=True)
        validators.validate_tag(tag=tag, none_ok=True)
        validators.validate_retry(retry=retry, none_ok=True)
        validators.validate_cache(cache=self.cache)

        try:
            with self.cache as ref:
                ref.set(
                    key=key, value=val, expire=expire, read=read, tag=tag, retry=retry
                )

        except Exception as exc:
            msg = Exception(
                f"Unhandled exception setting key/value pair for key: [{key}]. Details: {exc}"
            )
            log.error(msg)

            raise exc

    def get(
        self, key: t.Union[str, int, tuple, frozenset] = None, tags: list[str] = None
    ):
        """Search for a key in a given cache.

        Pass a diskcache.Cache object for cache, and a key (and optionally a list of tags).
        Function will search the cache and return a value if found, or a structured
        error dict describing the lack of key.

        Params:
            key (str): The key to search the cache for
            tags (list[str]): List of tags to search the cache for
        """
        validators.validate_key(key)
        validators.validate_cache(self.cache)
        validators.validate_tags(tags)

        try:
            if self.check_key_exists(key=key):
                try:
                    with self.cache as ref:
                        _val = ref.get(key=key)

                        return _val

                except Exception as exc:
                    msg = Exception(
                        f"Unhandled exception retrieving value of key [{key}]. Details: {exc}"
                    )
                    log.error(msg)

                    raise exc

            else:
                # return {
                #     "error": "Key not found in cache",
                #     "details": {"key": key, "cache_dir": self.cache.directory},
                # }

                return

        except Exception as exc:
            msg = Exception(
                f"Unhandled exception checking cache for key '{key}'. Details: {exc}"
            )
            log.error(msg)

            return None

    def set_expire(
        self, key: t.Union[str, int, tuple, frozenset] = None, expire: int = None
    ) -> dict[str, str] | None:
        """Set an expiration timeout (in seconds).

        Params:
            key (str): Name of the key to set expiration on. Must already exist in the cache.
            expire (int): Time (in seconds) to wait before expiring cached value.
        """
        validators.validate_key(key)
        validators.validate_cache(self.cache)
        validators.validate_expire(expire)

        if not self.check_key_exists(key=key):
            log.warning(
                f"Cache item with key [{key}] does not exist in cache at {self.cache.directory}/"
            )

            return None

        try:
            with self.cache as ref:
                ref.touch(key, expire=expire)

        except Exception as exc:
            msg = Exception(
                f"Unhandled exception setting expiration of {expire} on key [{key}] in cache at {self.cache.directory}/. Details: {exc}"
            )
            log.error(msg)

            raise exc

    def delete(
        self, key: t.Union[str, int, tuple, frozenset] = None, tag: str = None
    ) -> tuple:
        """Delete a cached value.

        If a tag is provided, only keys that also have that tag will be deleted.

        Params:
            key (str|int): Name of key in cache.
        """
        validators.validate_key(key)
        validators.validate_cache(self.cache)
        validators.validate_tag(tag)

        try:
            with self.cache as ref:
                _delete = ref.pop(key=key, tag=tag)

                return _delete

        except Exception as exc:
            msg = Exception(
                f"Unhandled exception deleting key {key} from cache at {self.cache.directory}/. Details: {exc}"
            )
            log.error(msg)

            raise exc

    def cull(self, retry: bool = False) -> bool:
        """Cull items from cache to free space.

        Params:
            retry (bool): When `True`, cull will be retried if a database timeout occurs.

        Returns:
            (bool): `True` if culling successful, otherwise `False`.

        """
        try:
            self.cache.cull(retry=retry)

            return True
        except Exception as exc:
            msg = Exception(f"Unhandled exception culling cache. Details: {exc}")
            log.error(msg)

            return False

    def get_cache_size(self) -> int:
        """Get a dict describing the size of the cache, in bytes.

        Returns:
            (int): An integer representing the cache's size in bytes.`

        """
        validators.validate_cache(cache=self.cache)

        try:
            cache_size: int = self.cache.volume()

            # return {"unit": "bytes", "size": cache_size}

            return cache_size

        except Exception as exc:
            msg = Exception(f"Unhandled exception getting cache size. Details: {exc}")
            log.error(msg)

            raise exc

    def healthcheck(self) -> list[warnings.WarningMessage]:
        """Run checks on Cache instance.

        Returns:
            (list[warning.WarningMessage]): A list of Diskcache `WarningMessage` objects.

        """
        validators.validate_cache(cache=self.cache)

        try:
            warnings = self.cache.check()

            return warnings

        except Exception as exc:
            msg = Exception(
                f"Unhandled exception checking cache for warnings. Details: {exc}"
            )
            log.error(msg)

            raise exc


class FanoutDiskCacheController(AbstractContextManager):
    def __init__(self):
        pass

    def __enter__(self):
        raise NotImplementedError("Fanout DiskCache controller not fully implemented")

    def __exit__(self, exc_type, exc_val, traceback):
        pass
