from punq import Container

from src.sitetracking.service import MyService, Dependency


def register_services(container: Container):
    container.register(Dependency)
    container.register(MyService)