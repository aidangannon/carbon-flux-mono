from mypy_boto3_dynamodb.service_resource import Table
from responses import RequestsMock

from src.carbon_tracking_service.core import TrackedSite
from src.common.handlers import LambdaHandle
from tests import BaseBddContext, LogCapture
from tests.carbon_tracking_service.service_tests.infrastructure.api_mocks.icos import Submission


class GetLatestSubmissionsContext(BaseBddContext):
    sut: LambdaHandle
    lambda_return: dict
    table: Table
    log_capture: LogCapture
    requests_mock: RequestsMock
    tracked_sites: list[TrackedSite]
    submissions: dict[str, Submission]
    scoped_log_vars: dict