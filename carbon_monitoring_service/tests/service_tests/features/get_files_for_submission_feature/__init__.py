from mypy_boto3_dynamodb.service_resource import Table
from responses import RequestsMock

from carbon_monitoring_service.src.core import MonitoredSite
from lambda_common.handlers import LambdaHandle
from pyight_bdd import BaseBddContext, LogCapture


class ResolveFluxSubmissionContext(BaseBddContext):
    sut: LambdaHandle
    requests_mock: RequestsMock
    log_capture: LogCapture
    result: dict
    submission_id: str
    site: str
    table: Table
    submission_timestamp: int
    file_urls: list[str]
    scoped_log_vars: dict
    monitored_site: MonitoredSite
