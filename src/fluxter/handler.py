from punq import Container

from src.common.handlers import lazy_handler_factory
from src.fluxter.bootstrap import bootstrap
from src.fluxter.services import MyService


def inner_handle(
    container: Container,
    event: dict,
    context: dict
) -> dict:
    from src.common.logging import Logger
    logger = container.resolve(Logger)
    print("hello")
    logger.info("Direct logger test from handler")
    service = container.resolve(MyService)
    response = service()
    return {
        "inner": response
    }

handle = lazy_handler_factory(
    inner_handler=inner_handle,
    ioc_registrar=bootstrap
)