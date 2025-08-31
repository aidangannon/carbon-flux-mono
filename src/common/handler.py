from typing import Callable, Any

from punq import Container

_container = None

LambdaHandler = Callable[[Container, dict, dict], dict]
IocFunc = Callable[[Container], None]

def lazy_handler_factory(
    inner_handler: LambdaHandler,
    ioc_registrar: IocFunc,
):
    global _container
    if _container is None:
        _container = Container()
        ioc_registrar(_container)

    def handler(event, context) -> dict:
        return inner_handler(_container, event, context)
    return handler