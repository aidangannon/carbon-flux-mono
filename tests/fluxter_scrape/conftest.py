from typing import Generator

import boto3
from moto import mock_aws
from mypy_boto3_dynamodb.type_defs import KeySchemaElementTypeDef, AttributeDefinitionTypeDef
from punq import Container
from pytest import fixture

from src.common.handlers import LambdaHandle
from src.fluxter_scrape.bootstrap import bootstrap
from src.fluxter_scrape.handler import inner_handle
from tests import add_test_logging


@fixture(scope='session', autouse=True)
def setup_database():
    print("setup_database")
    with mock_aws():
        print("inner setup_database")
        dynamodb = boto3.resource('dynamodb')
        dynamodb.create_table(
            TableName='fluxter-db',
            AttributeDefinitions=[
                AttributeDefinitionTypeDef(AttributeName="partition_key", AttributeType='S'),
                AttributeDefinitionTypeDef(AttributeName="id", AttributeType='S')
            ],
            KeySchema=[
                KeySchemaElementTypeDef(AttributeName='partition_key', KeyType='HASH'),
                KeySchemaElementTypeDef(AttributeName='id', KeyType='RANGE')
            ],
            BillingMode='PAY_PER_REQUEST'
        )
        yield

@fixture(scope='session', autouse=True)
def setup_handle(setup_database):
    print("setup_handle")
    container = Container()
    bootstrap(container=container)
    add_test_logging(container=container)
    yield lambda event, context: inner_handle(
        container=container,
        event=event,
        context=context)