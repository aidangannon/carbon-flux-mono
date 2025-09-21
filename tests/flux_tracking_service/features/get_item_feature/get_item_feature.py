from dataclasses import dataclass

from tests import scenario, fixture
from tests.flux_tracking_service.features.get_item_feature.get_item_feature_steps import data_exists_in_the_db, \
    lambda_is_called_with_data_id, lambda_response_should_equal_data, no_data_exists, lambda_response_should_be_empty, \
    needless_step_to_test_our_args, \
    data_exists_in_the_db_with_other_partition_PARTITION_and_number_NUMBER_and_person_PERSON
from tests.flux_tracking_service.infrastructure.common_steps.log_steps import \
    there_should_be_an_LEVEL_log_with_message_MESSAGE


@scenario
def test_1(get_item_feature):
    ctx = get_item_feature
    ctx.runner \
        .given(data_exists_in_the_db(ctx)) \
        .when(lambda_is_called_with_data_id(ctx)) \
        .then(lambda_response_should_equal_data(ctx)) \
        .and_also(there_should_be_an_LEVEL_log_with_message_MESSAGE(ctx, "Logging from service", "INFO")) \
        .run()

@scenario
def test_2(get_item_feature):
    ctx = get_item_feature
    ctx.runner \
        .given(no_data_exists()) \
        .when(lambda_is_called_with_data_id(ctx)) \
        .then(lambda_response_should_be_empty(ctx)) \
        .and_also(lambda_response_should_be_empty(ctx)) \
        .run()

@scenario
def test_another_blady_test(get_item_feature):
    ctx = get_item_feature
    ctx.runner \
        .given(data_exists_in_the_db_with_other_partition_PARTITION_and_number_NUMBER_and_person_PERSON(ctx, "123", 2, {"name": "", "blah": "new", "attributes": {}})) \
        .when(lambda_is_called_with_data_id(ctx)) \
        .then(lambda_response_should_be_empty(ctx)) \
        .and_also(lambda_response_should_be_empty(ctx)) \
        .and_also(needless_step_to_test_our_args(ctx, 2, "123")) \
        .run()


@dataclass(frozen=True, slots=True, unsafe_hash=True)
class Address:
    field1: str

@dataclass(frozen=True, slots=True, unsafe_hash=True)
class Person:
    name: str
    age: int
    attributes: dict
    list_of_strings: list[str]
    address: Address
    addresses: list[Address]

def test_something():
    person = fixture.create(Person)
    print(person)