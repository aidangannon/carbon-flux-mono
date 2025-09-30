from punq import Container

from src.common.logging import add_logging
from src.flux_tracking_service.flux_submission_resolver.config import IcosSettings


def bootstrap(container: Container):
    add_logging(container)
    add_settings(container)

def add_settings(container: Container):
    container.register(IcosSettings)