from punq import Container

from src.common.logging import add_logging


def bootstrap(container: Container):
    add_logging(container)