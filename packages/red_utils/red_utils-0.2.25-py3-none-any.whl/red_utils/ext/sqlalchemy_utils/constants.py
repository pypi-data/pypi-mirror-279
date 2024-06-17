"""Validators for custom SQLAlchemy utilities.

`valid_db_types`: List of strings of supported database types.

Supported: `["sqlite", "postgres", "mssql"]`
"""

## List of valid/supported databases
from __future__ import annotations

valid_db_types: list[str] = ["sqlite", "postgres", "mssql"]
