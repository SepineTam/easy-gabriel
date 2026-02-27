import asyncio

from typing import Callable, Coroutine


def run_gabriel(func: Callable | Coroutine, *args, **kwargs):
    if isinstance(func, Coroutine):
        return _asyncio_run(func)
    elif isinstance(func, Callable):
        return _asyncio_run(func(*args, **kwargs))
    else:
        raise TypeError("func must be a function or a coroutine")


def _asyncio_run(coroutine: Coroutine):
    return asyncio.run(coroutine)
