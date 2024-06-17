"""Utilities & methods for interacting with the `DiskCache` library."""

from . import validators, controllers
from .controllers import DiskCacheController, FanoutDiskCacheController

from .classes import CacheInstance
from .constants import TimeoutConf
from .__defaults import (
    default_cache_conf,
    default_timeout_dict,
    DEFAULT_CACHE_TIMEOUT,
    CACHE_DIR,
)
from .__defaults import TimeoutConf

from .__methods import (
    check_cache,
    check_cache_key_exists,
    clear_cache,
    convert_to_seconds,
    delete_val,
    get_cache_size,
    get_val,
    manage_cache_tag_index,
    new_cache,
    set_expire,
    set_val,
)
