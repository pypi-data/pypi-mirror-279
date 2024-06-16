"""Utilities for DataFrame libraries like `pandas` and `polars`.
"""

from __future__ import annotations

import pkgutil

from . import validators

if pkgutil.find_loader("pandas"):
    from . import pandas_utils

if pkgutil.find_loader("polars"):
    from . import polars_utils
