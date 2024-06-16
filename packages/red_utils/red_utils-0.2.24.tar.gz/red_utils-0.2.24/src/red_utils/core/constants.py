"""Constants for use as default values throughout `red_utils`.

Other modules import from `red_utils.core` to set values like the
default `DATA_DIR` (.data).
"""

from __future__ import annotations

from pathlib import Path

DATA_DIR: Path = Path(".data")
CACHE_DIR: Path = Path(f"{DATA_DIR}/.cache")
SERIALIZE_DIR: Path = Path(f"{DATA_DIR}/.serialize")
JSON_DIR: Path = Path(f"{DATA_DIR}/json")
LOG_DIR: Path = Path("logs")
DB_DIR: Path = Path(".db")

ENSURE_EXIST_DIRS: list[Path] = [DATA_DIR, CACHE_DIR, SERIALIZE_DIR, LOG_DIR]
