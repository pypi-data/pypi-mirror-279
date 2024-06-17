"""Context manager classes/functions.

These context managers can be used as `with` statements to provide a handler for a task. For example,
the `SimpleSpinner` class in `red_utils.ext.context_managers.cli_spinners` adds a CLI spinner to a
function running within  a `with SimpleSpinner()` statement:

``` py title="SimpleSpinner() context managers" linenums="1"
with SimpleSpinner("Demo spinner... "):
    time.sleep(15)
```

"""

from __future__ import annotations

import pkgutil

if pkgutil.find_loader("rich"):
    from . import cli_spinners
    from .cli_spinners import SimpleSpinner
