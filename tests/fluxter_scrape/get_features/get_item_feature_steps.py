import uuid

from assertpy import assert_that
from mypy_boto3_dynamodb.service_resource import Table
from pytest import fixture

from src.common.handlers import LambdaHandle
from tests import ScenarioRunner


class TestScenarioSteps:
    runner: ScenarioRunner
    sut: LambdaHandle
    table: Table
    item: dict
    response: dict
    item_id: str

    @fixture(autouse=True)
    def setup_class(self, setup_handle, setup_database):
        self.runner = ScenarioRunner()
        self.sut = setup_handle
        self.table = setup_database
        self.item_id = str(uuid.uuid4())

    def no_data_exists(self):
        ...

    def data_exists_in_the_db(self):
        self.item = {
            'partition_key': 'item',
            'id': self.item_id,
            'other_field': 'data',
            'number_field': 123
        }
        self.table.put_item(Item=self.item)

    def lambda_is_called_with_data_id(self):
        self.response = self.sut({
            "id": self.item_id,
            "partition_key": "item"
        }, {})

    def lambda_response_should_equal_data(self):
        assert_that(self.response["item"]).is_equal_to(self.item)

    def lambda_response_should_be_empty(self):
        assert_that(self.response["item"]).is_none()