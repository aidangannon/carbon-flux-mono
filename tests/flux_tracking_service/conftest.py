import responses

import boto3
from moto import mock_aws
from mypy_boto3_dynamodb.type_defs import KeySchemaElementTypeDef, AttributeDefinitionTypeDef
from punq import Container
from pytest import fixture

from src.common.handlers import InnerLambdaHandle, IocHandle
from src.flux_tracking_service.ingest.bootstrap import bootstrap
from src.flux_tracking_service.ingest.handler import inner_handle
from tests import add_test_logging
from tests.common import create_container_with_bootstrap, create_handler_with_inner_handle
from tests.flux_tracking_service.infrastructure.config import override_settings


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
  with responses.RequestsMock(assert_all_requests_are_fired=False) as requests_mock:
      yield requests_mock

@fixture(scope='session')
def ingest_container(database):
    return create_container_with_bootstrap(bootstrap)

@fixture(scope='session')
def ingest_settings(ingest_container):
    return override_settings(ingest_container)

@fixture(scope='session')
def ingest_handler(ingest_settings):
    return create_handler_with_inner_handle(ingest_settings, inner_handle)