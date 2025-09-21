from punq import Container

from src.common.handlers import lazy_handler_factory
from src.flux_tracking_service.ingest.bootstrap import bootstrap


def inner_handle(
    container: Container,
    event: dict,
    context: dict
) -> dict:
    return {
        "submissions": []
    }

handle = lazy_handler_factory(
    inner_handler=inner_handle,
    ioc_registrar=bootstrap
)