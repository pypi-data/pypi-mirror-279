from __future__ import annotations

import uuid

from .type_classes import CompatibleUUID

import sqlalchemy as sa
import sqlalchemy.orm as so
from typing_extensions import Annotated

## Annotated auto-incrementing integer primary key column
INT_PK = Annotated[
    int, so.mapped_column(sa.INTEGER, primary_key=True, autoincrement=True, unique=True)
]

## SQLAlchemy multi-database compatible UUID primary key
UUID_PK = Annotated[
    uuid.UUID,
    so.mapped_column(
        CompatibleUUID, primary_key=True, unique=True, insert_default=uuid.uuid4
    ),
]

## SQLAlchemy CHAR(2)
STR_2 = Annotated[str, so.mapped_column(sa.CHAR(2))]
## SQLAlchemy VARCHAR(10)
STR_10 = Annotated[str, so.mapped_column(sa.VARCHAR(10))]
## SQLAlchemy CHAR(32)
STR_32 = Annotated[str, so.mapped_column(sa.CHAR(32))]
## SQLAlchemy CHAR(36)
STR_36 = Annotated[str, so.mapped_column(sa.CHAR(36))]
## SQLAlchemy VARCHAR(255)
STR_255 = Annotated[str, so.mapped_column(sa.VARCHAR(255))]
