from punq import Container

from src.sitetracking.services import MyService, Dependency


def bootstrap(container: Container):
    container.register(Dependency)
    container.register(MyService)