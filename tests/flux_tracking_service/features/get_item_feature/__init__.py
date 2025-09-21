from punq import Container

from src.common.handlers import LambdaHandle
from mypy_boto3_dynamodb.service_resource import Table

from tests import BaseBddContext


class GetItemContext(BaseBddContext):
    sut: LambdaHandle
    container: Container
    table: Table
    response: dict
    item_id: str
    scoped_vars: dict
    item: dict