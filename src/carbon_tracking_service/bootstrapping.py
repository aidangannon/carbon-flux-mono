from typing import TypeVar, Type

from src.carbon_tracking_service.application import ports
from src.carbon_tracking_service.infrastructure.adapters import icos_flux_client
from src.carbon_tracking_service.infrastructure.adapters import dynamo_tracked_site_repository


__all__ = ["container"]


T = TypeVar("T")

class Container:
    """tiny container for our ports/adapters"""

    def __init__(self):
        self.dependencies = {}

    def __getitem__(self, key: Type[T]) -> T:
        return self.dependencies[key]

    def __setitem__(self, key: Type[T], value: T) -> None:
        self.dependencies[key] = value

container = Container()
container[ports.TrackedSiteRepository] = dynamo_tracked_site_repository
container[ports.FluxClient] = icos_flux_client