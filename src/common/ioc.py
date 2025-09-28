from typing import TypeVar, Type

from punq import Container

T = TypeVar('T')

def resolve_service(container: Container, service: Type[T]) -> T:
    return container.resolve(service)