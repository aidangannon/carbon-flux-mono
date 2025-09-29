from datetime import datetime

from mypy_boto3_dynamodb.service_resource import Table
from punq import Container
from responses import RequestsMock

from src.common.handlers import LambdaHandle
from src.flux_tracking_service.core import TrackedSite
from tests import BaseBddContext
from tests.flux_tracking_service.service_tests.infrastructure.api_mocks.icos import Submission


class DiscoverFluxSubmissionsContext(BaseBddContext):
    sut: LambdaHandle
    lambda_return: dict
    table: Table
    requests_mock: RequestsMock
    station: str
    tracked_sites: list[TrackedSite]
    submissions: dict[str, Submission]
    container: Container
    scoped_log_vars: dict