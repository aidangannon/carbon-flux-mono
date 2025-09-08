from tests.fluxter_scrape.scrapey_scrape.scrapey_scrape_steps import TestScenarioSteps


class TestScenario(TestScenarioSteps):

    def test(self):
        self.runner.run(
            given=self.data_exists_in_the_db(),
            when=self.lambda_is_called_with_data_id(),
            then=self.lambda_response_should_equal_data()
        )

    def test_2(self):
        self.runner.run(
            given=self.no_data_exists(),
            when=self.lambda_is_called_with_data_id(),
            then=self.lambda_response_should_be_empty()
        )