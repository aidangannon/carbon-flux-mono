from tests.fluxter_scrape.get_item_feature.conftest import data_exists_in_the_db, \
    lambda_is_called_with_data_id, lambda_response_should_equal_data, no_data_exists, lambda_response_should_be_empty, \
    get_item_feature, data_exists_in_the_db_PERSON_with_other_partition_PARTITION_KEY, needless_step_to_test_our_args, \
    Person


def test(get_item_feature):
    runner = get_item_feature.runner
    runner \
        .given(data_exists_in_the_db) \
        .when(lambda_is_called_with_data_id) \
        .then(lambda_response_should_equal_data) \
        .run()

def test_2(get_item_feature):
    runner = get_item_feature.runner
    runner \
        .given(no_data_exists) \
        .when(lambda_is_called_with_data_id) \
        .then(lambda_response_should_be_empty) \
        .and_also(lambda_response_should_be_empty) \
        .run()

def test_another_blady_test(get_item_feature):
    runner = get_item_feature.runner
    runner \
        .given_with_params(data_exists_in_the_db_PERSON_with_other_partition_PARTITION_KEY, "item2", number=4, person=Person(name="<NAME>", blah="blahdebar", attributes={"name": "killer"})) \
        .when(lambda_is_called_with_data_id) \
        .then(lambda_response_should_be_empty) \
        .and_also(lambda_response_should_be_empty) \
        .and_also_with_params(needless_step_to_test_our_args, "item2", number=2, _id="five") \
        .run()