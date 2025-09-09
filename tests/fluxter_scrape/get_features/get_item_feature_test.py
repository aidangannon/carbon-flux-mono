from tests.fluxter_scrape.get_features.conftest import data_exists_in_the_db, \
    lambda_is_called_with_data_id, lambda_response_should_equal_data, no_data_exists, lambda_response_should_be_empty, get_item_feature


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