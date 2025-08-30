from unittest import TestCase
from unittest.mock import Mock, MagicMock

from src.common import MyService, Dependency


class TestThis(TestCase):

    def setUp(self):
        self.__dep1 = MagicMock()
        self.__sut = MyService(self.__dep1)

    def test_my_stuff(self):
        self.__sut()
        self.__dep1.assert_called_once()