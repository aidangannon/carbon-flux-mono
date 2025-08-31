from unittest import TestCase
from unittest.mock import MagicMock

from punq import Container

import src
from src.sitetracking.bootstrap import register_services
from src.sitetracking.handler import handle
from src.sitetracking.service import Dependency


class TestThis(TestCase):

    def setUp(self):
        import src.common.handler
        src.common.handler._container = None  # Reset the global container
        
        inner_registrar = register_services
        def wrapped_registrar(container: Container):
            inner_registrar(container)
            container.register(Dependency, instance=MagicMock(return_value="Fake response"))
        src.sitetracking.bootstrap.register_services = wrapped_registrar

    def test_my_stuff(self):
        # act
        resp = handle({}, {})

        # assert
        with self.subTest("assert response"):
            self.assertEqual(resp, { "inner": "Fake response" })
