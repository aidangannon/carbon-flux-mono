from mypy_boto3_dynamodb.service_resource import Table
from responses import RequestsMock

from carbon_tracking_service.src.core import TrackedSite
from lambda_common.handlers import LambdaHandle
from pyight_bdd import BaseBddContext, LogCapture
from carbon_tracking_service.tests.service_tests.infrastructure.api_mocks.icos import Submission


class GetLatestSubmissionsContext(BaseBddContext):
    sut: LambdaHandle
    lambda_return: dict
    table: Table
    log_capture: LogCapture
    requests_mock: RequestsMock
    tracked_sites: list[TrackedSite]
    submissions: dict[str, Submission]
    scoped_log_vars: dict
