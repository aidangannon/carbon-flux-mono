from punq import Container

from src.common.handlers import lazy_handler_factory
from src.fluxter_scrape.bootstrap import bootstrap
from src.fluxter_scrape.services import MyService


def inner_handle(
    container: Container,
    event: dict,
    context: dict
) -> dict:
    service = container.resolve(MyService)
    response = service(item_id=event.get("id", "bumbaclart"))
    return {
        "item": response
    }

handle = lazy_handler_factory(
    inner_handler=inner_handle,
    ioc_registrar=bootstrap
)