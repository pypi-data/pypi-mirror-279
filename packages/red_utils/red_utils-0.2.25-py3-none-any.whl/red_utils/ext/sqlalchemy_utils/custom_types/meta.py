from __future__ import annotations

import uuid

from .type_classes import CompatibleUUID

from typing_extensions import Type

TYPEMAP_COMPATIBLE_UUID: dict[Type[uuid.UUID], Type[CompatibleUUID]] = {
    uuid.UUID: CompatibleUUID
}
