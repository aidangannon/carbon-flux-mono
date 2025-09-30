from punq import Container, Scope

from src.common.logging import add_logging
from src.flux_tracking_service.config import DynamoSettings
from src.flux_tracking_service.flux_submission_detector.application import FetchNewFluxFilesToProcess
from src.flux_tracking_service.flux_submission_detector.config import IcosSettings
from src.flux_tracking_service.flux_submission_detector.core import GetLatestSubmissionFeed, GetAllTrackedSites
from src.flux_tracking_service.flux_submission_detector.infrastructure.dynamo import DynamoGetAllTrackedSites
from src.flux_tracking_service.flux_submission_detector.infrastructure.icos import IcosGetLatestSubmissionFeed


def bootstrap(container: Container):
    add_logging(container)
    add_settings(container)
    add_application(container)
    add_infrastructure(container)

def add_settings(container: Container):
    container.register(IcosSettings, instance=IcosSettings(), scope=Scope.singleton)
    container.register(DynamoSettings, instance=DynamoSettings(), scope=Scope.singleton)

def add_application(container: Container):
    container.register(FetchNewFluxFilesToProcess, scope=Scope.singleton)

def add_infrastructure(container: Container):
    container.register(GetLatestSubmissionFeed, IcosGetLatestSubmissionFeed, scope=Scope.singleton)
    container.register(GetAllTrackedSites, DynamoGetAllTrackedSites, scope=Scope.singleton)