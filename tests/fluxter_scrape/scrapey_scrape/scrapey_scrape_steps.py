from typing import Callable

from punq import Container

from src.fluxter_scrape.bootstrap import bootstrap
from src.fluxter_scrape.handler import inner_handle
from tests import BaseScenario, step


class MyTestScenario(BaseScenario):

    def setup_scenario(self):
        container = Container()
        bootstrap(container=container)
        self.sut = inner_handle

    @step
    def given_this_is_a_test(self):
        self.sut()