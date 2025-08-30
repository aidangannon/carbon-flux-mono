from unittest import TestCase
from unittest.mock import Mock, MagicMock

import src.sitetracking.handler
from src.common import MyService, Dependency
from src.sitetracking.handler import handle


class TestThis(TestCase):

    def setUp(self):
        src.sitetracking\
            .handler\
            .container\
            .register(Dependency, instance=MagicMock(return_value="Fake response"))

    def test_my_stuff(self):
        # act
        resp = handle({}, {})

        # assert
        with self.subTest("assert response"):
            self.assertEqual(resp, { "inner": "Fake response" })
