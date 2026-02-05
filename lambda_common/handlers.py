from typing import Protocol


class LambdaHandle(Protocol):
    def __call__(self, event: dict, context: dict) -> dict: ...