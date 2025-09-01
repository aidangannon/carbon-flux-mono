from unittest import TestCase
from unittest.mock import MagicMock

from punq import Container

from src.fluxter.bootstrap import bootstrap
from src.fluxter.handler import inner_handle
from src.fluxter.services import Dependency


class TestThis(TestCase):

    def setUp(self):
        self.container = Container()
        bootstrap(container=self.container)
        self.container.register(Dependency, instance=MagicMock(return_value="Fake response"))

    def test_my_stuff(self):
        # act
        resp = inner_handle(self.container, {}, {})

        # assert
        with self.subTest("assert response"):
            self.assertEqual(resp, { "inner": "Fake response" })
