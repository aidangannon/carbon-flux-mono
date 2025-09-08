from tests.fluxter_scrape.get_features.get_item_feature_steps import TestScenarioSteps


class TestScenario(TestScenarioSteps):

    def test(self):
        self.runner\
            .given(self.data_exists_in_the_db) \
            .when(self.lambda_is_called_with_data_id) \
            .then(self.lambda_response_should_equal_data) \
            .run()

    def test_2(self):
        self.runner \
            .given(self.no_data_exists) \
            .when(self.lambda_is_called_with_data_id) \
            .then(self.lambda_response_should_be_empty) \
            .and_also(self.lambda_response_should_be_empty) \
            .run()