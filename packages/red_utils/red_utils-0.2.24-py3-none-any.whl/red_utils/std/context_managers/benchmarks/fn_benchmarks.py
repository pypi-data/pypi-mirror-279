from __future__ import annotations

import logging

log = logging.getLogger("red_utils.std.context_managers.benchmarks")

from contextlib import asynccontextmanager, contextmanager
import time

@contextmanager
def benchmark(description: str = "Unnamed function timer") -> None:
    """Time an operation.

    Run an operation with this context manager (`with benchmark("time some function"):`) to time function execution.

    Params:
        description (str): A string that prints while the benchmark is running. This can be a message to the user, like
            "benchmarking move_files()", or a message like "this will take a while...".
            Once the benchmark finishes, details about the benchmarked function's execution will be printed to the terminal.

    Usage:
    ``` py linenums="1"
    with benchmark("Short description here"):
        some_function()
    ```
    """
    start = time.time()
    yield
    elapsed = time.time() - start

    print(f"{description}: {elapsed} seconds")


@asynccontextmanager
async def async_benchmark(description: str = "Unnamed async function timer") -> None:
    """Time an asynchronous operation.

    Run an async function/operation with this context manager to time function execution.

    Params:
        description (str): A string that prints while the benchmark is running. This can be a message to the user, like
            "benchmarking move_files()", or a message like "this will take a while...".
            Once the benchmark finishes, details about the benchmarked function's execution will be printed to the terminal.

    Usage:
    ``` py linenums="1"
    with async_benchmark("Short description here"):
        await some_async_function()
    ```
    """
    start = time.monotonic()

    try:
        yield
    finally:
        elapsed = time.monotonic() - start
        print(f"{description}: {elapsed}s")
