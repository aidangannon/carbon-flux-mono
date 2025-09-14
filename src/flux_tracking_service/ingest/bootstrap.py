from punq import Container

from src.common.logging import add_logging
from src.flux_tracking_service.ingest.services import MyService, Dependency, AnotherDependency


def bootstrap(container: Container):
    add_logging(container)
    container.register(Dependency)
    container.register(AnotherDependency)
    container.register(MyService)