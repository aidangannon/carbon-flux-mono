from punq import Container
from responses import RequestsMock

from src.common.handlers import LambdaHandle
from tests import BaseBddContext


class ResolveFluxSubmissionContext(BaseBddContext):
    sut: LambdaHandle
    requests_mock: RequestsMock
    container: Container
    result: dict
    scoped_log_vars: dict