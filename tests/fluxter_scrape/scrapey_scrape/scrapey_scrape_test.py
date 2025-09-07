from tests.fluxter_scrape.scrapey_scrape.scrapey_scrape_steps import TestScenarioSteps


class TestScenario(TestScenarioSteps):

    def test_some_stuff1(self):
        print("test_some_stuff1")
        self.given_add_some_data()\
            .when_this()\
            .then_that()

    def test_some_stuff2(self):
        print("test_some_stuff2")
        self.given_add_some_data()\
            .when_this()\
            .then_that()