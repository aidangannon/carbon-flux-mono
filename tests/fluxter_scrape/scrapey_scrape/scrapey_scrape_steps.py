import uuid
from dataclasses import dataclass
from typing import Generator

import boto3
from mypy_boto3_dynamodb.service_resource import Table
from pytest import fixture
from assertpy import assert_that

from src.common.handlers import LambdaHandle
from tests import step, ScenarioRunner


@dataclass(frozen=True, slots=True)
class Context:
    table: Table
    sut: LambdaHandle


@fixture(scope="class", autouse=True)
def setup_scenario(setup_handle):
    print("setup_scenario")
    yield Context(
        table=boto3\
            .resource('dynamodb')\
            .Table('fluxter-db'),
        sut=setup_handle
    )


class TestScenarioSteps:
    runner: ScenarioRunner
    context: Context

    def setup_method(self, setup_scenario):
        self.context = setup_scenario

    @step
    def given_add_some_data(self) -> 'TestScenarioSteps':
        self.item = {
            'partition_key': str(uuid.uuid4()),
            'id': str(uuid.uuid4()),
            'other_field': 'data',
            'number_field': 123
        }
        self.context.table.put_item(Item=self.item)
        return self

    @step
    def when_this(self) -> 'TestScenarioSteps':
        self.response = self.context.sut({
            "id": self.item["id"],
            "partition_key": self.item["partition_key"]
        }, {})
        return self

    @step
    def then_that(self) -> 'TestScenarioSteps':
        assert_that(self.response).is_equal_to(self.item)
        return self