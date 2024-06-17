"""CLI spinner context managers add an animated spinner to long-running tasks.

Example:
``` py title="SimpleSpinner() CLI" linenums="1"
with SimpleSpinner("Demo spinner... "):
    time.sleep(15)
```

"""

from __future__ import annotations

from . import handlers
from .handlers import SimpleSpinner
