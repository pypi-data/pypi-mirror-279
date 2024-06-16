"""Mixin classes for Python dataclasses.

Usage:

Define a class that inherits from one or more mixins. For example, to inherit from `DictMixin`:

``` py title="schemas.py" linenums="1"
from red_utils.core.mixins import DictMixin
from dataclasses import dataclass

class ExampleClass(DictMixin):
    name: str = "human"
    
classobj = ExampleClass()
classobj.as_dict()  # classobj now has access to the `.as_dict()` method of `DictMixin`.
```
"""

from __future__ import annotations

from .mixin_classes import DictMixin
