from mypy_boto3_dynamodb.service_resource import Table
from responses import RequestsMock

from src.carbon_tracking_service.core import TrackedSite
from src.common.handlers import LambdaHandle
from tests import BaseBddContext, LogCapture


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
    tracked_site: TrackedSite