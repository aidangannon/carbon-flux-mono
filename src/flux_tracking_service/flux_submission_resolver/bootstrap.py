from punq import Container, Scope

from src.common.logging import add_logging
from src.flux_tracking_service.config import DynamoSettings
from src.flux_tracking_service.flux_submission_resolver.application import ResolveFilesForSubmission
from src.flux_tracking_service.flux_submission_resolver.config import IcosSettings
from src.flux_tracking_service.flux_submission_resolver.core import RetrieveFilesForSubmission, UpdateSiteLastFetched
from src.flux_tracking_service.flux_submission_resolver.infrastructure.dynamo import DynamoUpdateSiteLastFetched
from src.flux_tracking_service.flux_submission_resolver.infrastructure.icos import IcosRetrieveFilesForSubmission


def bootstrap(container: Container):
    add_logging(container)
    add_settings(container)
    add_application(container)
    add_infrastructure(container)

def add_settings(container: Container):
    container.register(IcosSettings, instance=IcosSettings(), scope=Scope.singleton)
    container.register(DynamoSettings, instance=DynamoSettings(), scope=Scope.singleton)

def add_application(container: Container):
    container.register(ResolveFilesForSubmission, scope=Scope.singleton)

def add_infrastructure(container: Container):
    container.register(RetrieveFilesForSubmission, IcosRetrieveFilesForSubmission, scope=Scope.singleton)
    container.register(UpdateSiteLastFetched, DynamoUpdateSiteLastFetched, scope=Scope.singleton)