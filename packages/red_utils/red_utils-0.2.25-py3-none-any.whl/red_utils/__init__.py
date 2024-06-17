"""Custom utilities for stdlib & select libraries.

Add utilities to your projects to add functionality like context managers for editing files,
lists, dicts, & more, SQLAlchemy helpers like a default `Base` class, functions to get SQLAlchemy
`Session`s and custom connection classes to handle database URIs & configuration, and much more.

!!! warning

    `red_utils` is a pet project, not meant to be used in any serious capacity. If you really want to use specific features/functions of `red_utils`,
    copy the code into your own project and rewrite it enough that it works with your app.

A collection of enhancements/utilities for modules & Python packages I use frequently. Modules are broken down into `std` and `ext`.
Modules in `red_utils.std` have no external dependencies, requiring only the Python `stdlib`. Modules in `red_utils.ext`, on the other
hand, are utilities & extensions I've written for packages like `Loguru`, `SQLAlchemy`, and `Pydantic`.

The reference documentation is automatically generated from comments in the code. If I have not added docstrings to a file/function/class, it will not
show up in the Reference section of this site. I'll get to it 🤷‍♂️
"""

from __future__ import annotations

import logging
import logging.handlers
import sys

from red_utils.std import logging_utils

## Set a nullhandler on the library's logger.
#  This is so the logger can be configured by the application that imports red_utils
logging.getLogger("red_utils").addHandler(logging.NullHandler())

sys.path.append(".")

from .exc import CustomException
