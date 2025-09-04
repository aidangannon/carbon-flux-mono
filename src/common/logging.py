import logging
from typing import Protocol, Any, ContextManager

import sys

from loguru import logger
from punq import Container, Scope


class Logger(Protocol):
    """
    non-implementation specific duck-type for the logger
    """
    def info(self, msg: str, *args: Any, **kwargs: Any) -> None: ...

    def warning(self, msg: str, *args: Any, **kwargs: Any) -> None: ...

    def error(self, msg: str, *args: Any, **kwargs: Any) -> None: ...

    def contextualize(self, *args: Any, **kwargs: Any) -> ContextManager[Any]: ...


def add_logging(container: Container):
    logger.remove()
    logger.add(sys.stdout, serialize=True)
    container.register(Logger, instance=logger, scope=Scope.singleton)