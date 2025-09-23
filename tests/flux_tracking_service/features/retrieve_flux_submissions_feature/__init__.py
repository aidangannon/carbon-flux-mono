from datetime import datetime

from mypy_boto3_dynamodb.service_resource import Table
from punq import Container
from responses import RequestsMock

from src.common.handlers import LambdaHandle
from tests import BaseBddContext


class RetrieveFluxSubmissionsContext(BaseBddContext):
    sut: LambdaHandle
    lambda_return: dict
    table: Table
    requests_mock: RequestsMock
    station: str
    submission: str
    container: Container