from tests import scenario
from tests.flux_tracking_service.features.get_item_feature.get_item_feature_steps import data_exists_in_the_db, \
    lambda_is_called_with_data_id, lambda_response_should_equal_data, no_data_exists, lambda_response_should_be_empty, \
    needless_step_to_test_our_args, data_exists_in_the_db_with_other_partition_PARTITION_and_number_NUMBER_and_person_PERSON


def test_1(get_item_feature):
    context = get_item_feature
    context.runner \
        .given(data_exists_in_the_db(context)) \
        .when(lambda_is_called_with_data_id(context)) \
        .then(lambda_response_should_equal_data(context)) \
        .run()

def test_2(get_item_feature):
    context = get_item_feature
    context.runner \
        .given(no_data_exists()) \
        .when(lambda_is_called_with_data_id(context)) \
        .then(lambda_response_should_be_empty(context)) \
        .and_also(lambda_response_should_be_empty(context)) \
        .run()

def test_another_blady_test(get_item_feature):
    context = get_item_feature
    context.runner \
        .given(data_exists_in_the_db_with_other_partition_PARTITION_and_number_NUMBER_and_person_PERSON(context, "123", 2, {"name": "", "blah": "new", "attributes": {}})) \
        .when(lambda_is_called_with_data_id(context)) \
        .then(lambda_response_should_be_empty(context)) \
        .and_also(lambda_response_should_be_empty(context)) \
        .and_also(needless_step_to_test_our_args(context, 2, "123")) \
        .run()