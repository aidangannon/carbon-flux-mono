from punq import Container, Scope

from src.common.logging import add_logging
from src.flux_tracking_service.config import DynamoSettings
from src.flux_tracking_service.ingest.application.commands import FetchNewFluxFilesToProcess
from src.flux_tracking_service.ingest.config import IcosSettings
from src.flux_tracking_service.ingest.core import GetFileUrlsForSite, GetAllTrackedSites
from src.flux_tracking_service.ingest.infrastructure.dynamo import DynamoGetAllTrackedSites
from src.flux_tracking_service.ingest.infrastructure.icos import IcosGetFileUrlsForSite


def bootstrap(container: Container):
    add_logging(container)
    add_settings(container)
    add_application(container)
    add_infrastructure(container)

def add_settings(container: Container):
    container.register(
        IcosSettings,
        instance=IcosSettings(),
        scope=Scope.singleton
    )
    container.register(
        DynamoSettings,
        instance=DynamoSettings(),
        scope=Scope.singleton
    )

def add_application(container: Container):
    container.register(FetchNewFluxFilesToProcess, scope=Scope.singleton)

def add_infrastructure(container: Container):
    container.register(GetFileUrlsForSite, IcosGetFileUrlsForSite, scope=Scope.singleton)
    container.register(GetAllTrackedSites, DynamoGetAllTrackedSites, scope=Scope.singleton)