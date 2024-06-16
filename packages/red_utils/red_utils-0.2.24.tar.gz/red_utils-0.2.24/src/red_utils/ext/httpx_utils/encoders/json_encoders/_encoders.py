from __future__ import annotations

import logging

log = logging.getLogger("red_utils.ext.httpx_utils.encoders.json_encoders")

from datetime import datetime
import json
import typing as t

import pendulum

class DateTimeEncoder(json.JSONEncoder):
    """Handle encoding a `datetime.datetime` or `pendulum.DateTime` as an ISO-formatted string."""

    def default(self, o) -> str | json.Any:
        if isinstance(o, datetime):
            return o.isoformat()
        elif isinstance(o, pendulum.DateTime):
            return o.isoformat()

        try:
            _encoded = json.JSONEncoder.default(self=self, o=o)
        except Exception as exc:
            msg = Exception(f"Unhandled exception encoding DateTime. Details: {exc}")
            log.error(msg)

            raise exc

        return _encoded
