from unittest.mock import MagicMock

from assertpy import assert_that
from punq import Container

from src.fluxter_scrape.bootstrap import bootstrap
from src.fluxter_scrape.handler import inner_handle
from src.fluxter_scrape.services import Dependency


class TestThis:

    def setup_method(self):
        self.container = Container()
        bootstrap(container=self.container)
        self.container.register(Dependency, instance=MagicMock(return_value="Fake response"))

    def test_my_stuff(self):
        # act
        resp = inner_handle(self.container, {}, {})

        # assert
        assert_that(resp).is_equal_to({ "inner": "Fake response" })
