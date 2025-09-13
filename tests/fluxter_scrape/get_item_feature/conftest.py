from dataclasses import dataclass
from unittest.mock import Mock

from pytest import fixture
import uuid

from assertpy import assert_that
from mypy_boto3_dynamodb.service_resource import Table

from src.common.handlers import LambdaHandle
from src.fluxter.fluxter_scrape.services import AnotherDependency
from tests import BaseBddContext


@fixture
def get_item_feature(handler, container, database):
    context = TestScenarioContext()
    container.register(AnotherDependency, instance=Mock())
    context.sut = handler
    context.table = database
    context.item_id = str(uuid.uuid4())
    return context


@dataclass(unsafe_hash=True)
class Person:
    name: str
    blah: str
    attributes: dict


class TestScenarioContext(BaseBddContext):
    sut: LambdaHandle
    table: Table
    response: dict
    item_id: str
    item: dict


def no_data_exists():
        ...

def data_exists_in_the_db(context: TestScenarioContext):
    context.item = {
        'partition_key': 'item',
        'id': context.item_id,
        'other_field': 'data',
        'number_field': 123
    }
    context.table.put_item(Item=context.item)

def data_exists_in_the_db_PERSON_with_other_partition_PARTITION_KEY(
    context: TestScenarioContext,
    partition_key: str,
    number: int,
    person: Person
):
    context.item = {
        'partition_key': partition_key,
        'id': context.item_id,
        'other_field': 'data',
        'number_field': number
    }
    context.table.put_item(Item=context.item)

def needless_step_to_test_our_args(
    partition_key: str,
    number: int,
    _id: str
):
    _ = {
        'partition_key': partition_key,
        'id': _id,
        'other_field': 'data',
        'number_field': number
    }

def lambda_is_called_with_data_id(context: TestScenarioContext):
    context.response = context.sut({
        "id": context.item_id,
        "partition_key": "item"
    }, {})

def lambda_response_should_equal_data(context: TestScenarioContext):
    assert_that(context.response["item"]).is_equal_to(context.item)

def lambda_response_should_be_empty(context: TestScenarioContext):
    assert_that(context.response["item"]).is_none()