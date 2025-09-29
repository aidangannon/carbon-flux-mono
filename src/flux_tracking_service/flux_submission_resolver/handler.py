from punq import Container

from src.common.handlers import lazy_handler_factory
from src.flux_tracking_service.flux_submission_resolver.bootstrap import bootstrap


def inner_handle(container: Container, _: dict, __: dict) -> dict:
    return {}


handle = lazy_handler_factory(
    inner_handler=inner_handle,
    ioc_registrar=bootstrap
)