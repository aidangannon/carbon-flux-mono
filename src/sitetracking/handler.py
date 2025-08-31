from punq import Container

from src.common.handler import lazy_handler_factory
from src.sitetracking.bootstrap import register_services
from src.sitetracking.service import MyService


def inner_handle(
    container: Container,
    event: dict,
    context: dict
) -> dict:
    service = container.resolve(MyService)
    response = service()
    return {
        "inner": response
    }

handle = lazy_handler_factory(
    inner_handler=inner_handle,
    ioc_registrar=register_services
)