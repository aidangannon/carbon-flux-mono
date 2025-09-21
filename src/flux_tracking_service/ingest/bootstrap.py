from punq import Container, Scope

from src.common.logging import add_logging
from src.flux_tracking_service.ingest.config import IcosSettings


def bootstrap(container: Container):
    add_logging(container)

def add_settings(container: Container):
    container.register(
        IcosSettings,
        instance=IcosSettings(),
        scope=Scope.singleton
    )