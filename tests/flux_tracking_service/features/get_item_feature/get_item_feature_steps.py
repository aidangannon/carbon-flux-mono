from dataclasses import dataclass

from assertpy import assert_that
from mypy_boto3_dynamodb.service_resource import Table

from src.common.handlers import LambdaHandle
from tests import BaseBddContext, step
from tests.flux_tracking_service.features.get_item_feature import TestScenarioContext


@step
def no_data_exists():
        ...

@step
def data_exists_in_the_db(context: TestScenarioContext):
    context.item = {
        'partition_key': 'item',
        'id': context.item_id,
        'other_field': 'data',
        'number_field': 123
    }
    context.table.put_item(Item=context.item)

@step
def data_exists_in_the_db_with_other_partition_PARTITION_and_number_NUMBER_and_person_PERSON(
    context: TestScenarioContext,
    partition: str,
    number: int,
    person: dict
):
    context.item = {
        'partition_key': partition,
        'id': context.item_id,
        'other_field': 'data',
        'number_field': number
    }
    context.table.put_item(Item=context.item)

@step
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

@step
def lambda_is_called_with_data_id(context: TestScenarioContext):
    context.response = context.sut({
        "id": context.item_id,
        "partition_key": "item"
    }, {})

@step
def lambda_response_should_equal_data(context: TestScenarioContext):
    assert_that(context.response["item"]).is_equal_to(context.item)

@step
def lambda_response_should_be_empty(context: TestScenarioContext):
    assert_that(context.response["item"]).is_none()