from pytest import fixture
import uuid

from assertpy import assert_that
from mypy_boto3_dynamodb.service_resource import Table

from src.common.handlers import LambdaHandle
from tests import BaseBddContext


@fixture
def get_item_feature(handler, database):
    context = TestScenarioContext()
    context.sut = handler
    context.table = database
    context.item_id = str(uuid.uuid4())
    return context


class TestScenarioContext(BaseBddContext):
    sut: LambdaHandle
    table: Table
    response: dict
    item_id: str
    item: dict


def no_data_exists(context: TestScenarioContext):
        ...

def data_exists_in_the_db(context: TestScenarioContext):
    context.item = {
        'partition_key': 'item',
        'id': context.item_id,
        'other_field': 'data',
        'number_field': 123
    }
    context.table.put_item(Item=context.item)

def lambda_is_called_with_data_id(context: TestScenarioContext):
    context.response = context.sut({
        "id": context.item_id,
        "partition_key": "item"
    }, {})

def lambda_response_should_equal_data(context: TestScenarioContext):
    assert_that(context.response["item"]).is_equal_to(context.item)

def lambda_response_should_be_empty(context: TestScenarioContext):
    assert_that(context.response["item"]).is_none()