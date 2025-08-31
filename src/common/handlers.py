from typing import Callable, Any

from punq import Container

# internal cache for reuse
_container = None

LambdaHandle = Callable[[Container, dict, dict], dict]
IocHandle = Callable[[Container], None]

def lazy_handler_factory(
    inner_handler: LambdaHandle,
    ioc_registrar: IocHandle,
):
    global _container
    if _container is None:
        _container = Container()
        ioc_registrar(_container)

    def handler(event, context) -> dict:
        return inner_handler(_container, event, context)
    return handler