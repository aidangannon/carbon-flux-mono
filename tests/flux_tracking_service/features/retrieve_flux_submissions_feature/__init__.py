from mypy_boto3_dynamodb.service_resource import Table
from responses import RequestsMock

from src.common.handlers import LambdaHandle
from tests import BaseBddContext


class RetrieveFluxSubmissionsContext(BaseBddContext):
    sut: LambdaHandle
    lambda_return: dict
    table: Table
    requests_mock: RequestsMock
    station_id: str