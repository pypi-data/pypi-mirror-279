"""Extensions & utilities for third-party libraries I use frequently, like `red_utils.ext.sqla_utils`.

Contains boilerplate code for `SQLAlchemy`, or `red_utils.ext.pydantic`, which contains a method (parse_pydantic_schema) that can
parse a `Pydantic` class object into a compatible `SQLAlchemy` model.

This module uses `importlib.util.find_spec()` to only load modules if dependencies are met, keeping the `red_utils` package functional by limiting the utilities that are loaded.
If a find_spec() check fails, that import is passed over and will be unavailable
for type completion & usage.

This can lead to some odd behavior! For example, if you try to import `from red_utils.ext import time_utils`, but you do not have the `pendulum` dependency, you will get
exceptions about a missing module. If you import a 3rd party util library, make sure the dependency is installed! Check the project's `pyproject.toml`, or `requirements/requirements*.txt`.
"""
