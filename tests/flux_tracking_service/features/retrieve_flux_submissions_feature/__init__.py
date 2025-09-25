from datetime import datetime

from mypy_boto3_dynamodb.service_resource import Table
from punq import Container
from responses import RequestsMock

from src.common.handlers import LambdaHandle
from src.flux_tracking_service.core import TrackedSite
from src.flux_tracking_service.ingest.infrastructure.icos import Submission
from tests import BaseBddContext

class RetrieveFluxSubmissionsContext(BaseBddContext):
    sut: LambdaHandle
    lambda_return: dict
    table: Table
    requests_mock: RequestsMock
    station: str
    tracked_sites: list[TrackedSite]
    submission_contents: dict[str, Submission]
    container: Container
    scoped_log_vars: dict