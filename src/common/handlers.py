from functools import lru_cache
from typing import Callable, Any, Protocol

from punq import Container


class LambdaHandle(Protocol):
    def __call__(self, event: dict, context: dict) -> dict: ...