"""Custom exceptions used throughout `red_utils`. These exceptions can be imported & raised in your own code.

For example, to use `CustomException` as a base class for a new exception specific to your app:

``` py title="exceptions.py" linenums="1"
from red_utils.exc import CustomException

class MyException(CustomException):
    ## Class inherits the 'msg' and 'errors' class variables from CustomException.
    #  Define a new variable just for this exception
    level: int = 0
```
"""

from __future__ import annotations

from ._generic import CustomException
from .import_exc import CustomModuleNotFoundError, MissingDependencyException
