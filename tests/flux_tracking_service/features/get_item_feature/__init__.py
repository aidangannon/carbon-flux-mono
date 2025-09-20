from src.common.handlers import LambdaHandle
from mypy_boto3_dynamodb.service_resource import Table

from tests import BaseBddContext


class TestScenarioContext(BaseBddContext):
    sut: LambdaHandle
    table: Table
    response: dict
    item_id: str
    item: dict