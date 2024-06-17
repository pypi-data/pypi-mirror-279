"""The `core` module contains constants & utility functions meant for internal use. Other modules in `red_utils` can access the `red_utils.core`
package to call constants like `DATA_DIR` (defaults to `.data`) when setting default params for a function.
"""

from __future__ import annotations

from . import constants, dataclass_utils
from .constants import (
    CACHE_DIR,
    DATA_DIR,
    DB_DIR,
    ENSURE_EXIST_DIRS,
    JSON_DIR,
    LOG_DIR,
    SERIALIZE_DIR,
)
