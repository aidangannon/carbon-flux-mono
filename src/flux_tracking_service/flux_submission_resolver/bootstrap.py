from punq import Container, Scope

from src.common.logging import add_logging
from src.flux_tracking_service.config import DynamoSettings
from src.flux_tracking_service.flux_submission_resolver.config import IcosSettings


def bootstrap(container: Container):
    add_logging(container)
    add_settings(container)

def add_settings(container: Container):
    container.register(IcosSettings, instance=IcosSettings(), scope=Scope.singleton)
    container.register(DynamoSettings, instance=DynamoSettings(), scope=Scope.singleton)