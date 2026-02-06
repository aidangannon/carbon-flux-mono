from mypy_boto3_dynamodb.service_resource import Table
from responses import RequestsMock

from carbon_monitoring_service.src.core import MonitoredSite
from lambda_common.handlers import LambdaHandle
from pyight_bdd import BaseBddContext, LogCapture
from carbon_monitoring_service.tests.service_tests.infrastructure.api_mocks.icos import Submission


class GetLatestSubmissionsContext(BaseBddContext):
    sut: LambdaHandle
    lambda_return: dict
    table: Table
    log_capture: LogCapture
    requests_mock: RequestsMock
    monitored_sites: list[MonitoredSite]
    submissions: dict[str, Submission]
    scoped_log_vars: dict
