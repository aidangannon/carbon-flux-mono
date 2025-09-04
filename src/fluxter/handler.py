from punq import Container

from src.common.handlers import lazy_handler_factory
from src.fluxter.bootstrap import bootstrap
from src.fluxter.services import MyService


def inner_handle(
    container: Container,
    event: dict,
    context: dict
) -> dict:
    service = container.resolve(MyService)
    response = service()
    print("hello")
    return {
        "inner": response
    }

handle = lazy_handler_factory(
    inner_handler=inner_handle,
    ioc_registrar=bootstrap
)