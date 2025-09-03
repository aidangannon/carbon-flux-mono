from punq import Container

from src.common.logging import add_logging
from src.fluxter.services import MyService, Dependency


def bootstrap(container: Container):
    add_logging()
    container.register(Dependency)
    container.register(MyService)