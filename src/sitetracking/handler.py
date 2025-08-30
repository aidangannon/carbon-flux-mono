from punq import Container

from src.common import MyService, register_common

container = Container()
register_common(container)

def handle(event, context):
    service = container.register(MyService)
    return {
        "inner": service()
    }