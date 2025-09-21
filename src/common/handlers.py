from functools import lru_cache
from typing import Callable, Any, Protocol

from punq import Container


class LambdaHandle(Protocol):
    def __call__(self, event: dict, context: dict) -> dict: ...

InnerLambdaHandle = Callable[[Container, dict, dict], dict]
IocHandle = Callable[[Container], None]

@lru_cache(maxsize=1)
def get_container(ioc_registrar: IocHandle) -> Container:
    """
    for internal caching across lambdas
    """
    container = Container()
    ioc_registrar(container)
    return container


def lazy_handler_factory(
    inner_handler: InnerLambdaHandle,
    ioc_registrar: IocHandle,
) -> LambdaHandle:

    def handler(event, context) -> dict:
        return inner_handler(get_container(ioc_registrar), event, context)

    return handler