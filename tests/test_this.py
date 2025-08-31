from unittest import TestCase
from unittest.mock import MagicMock

from punq import Container

import src
from src.sitetracking.bootstrap import register_services
from src.sitetracking.handler import handle, inner_handle
from src.sitetracking.service import Dependency


class TestThis(TestCase):

    def setUp(self):
        self.container = Container()
        register_services(container=self.container)
        self.container.register(Dependency, instance=MagicMock(return_value="Fake response"))

    def test_my_stuff(self):
        # act
        resp = inner_handle(self.container, {}, {})

        # assert
        with self.subTest("assert response"):
            self.assertEqual(resp, { "inner": "Fake response" })
