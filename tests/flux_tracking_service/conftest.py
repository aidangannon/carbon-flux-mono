import responses

import boto3
from moto import mock_aws
from mypy_boto3_dynamodb.type_defs import KeySchemaElementTypeDef, AttributeDefinitionTypeDef
from punq import Container
from pytest import fixture

from src.flux_tracking_service.ingest.bootstrap import bootstrap
from src.flux_tracking_service.ingest.handler import inner_handle
from tests import add_test_logging


@fixture(scope='session')
def database():
    with mock_aws():
        dynamodb = boto3.resource('dynamodb', region_name='eu-west-2')
        yield dynamodb.create_table(
            TableName='flux-tracking-db',
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

@fixture(scope='session')
def api_mocks():
  with responses.RequestsMock() as requests_mock:
      yield requests_mock

@fixture(scope='session')
def container(database):
    container = Container()
    bootstrap(container=container)
    add_test_logging(container=container)
    return container

@fixture(scope='session')
def handler(container):
    container = container
    return lambda event, context: inner_handle(
        container=container,
        event=event,
        context=context)