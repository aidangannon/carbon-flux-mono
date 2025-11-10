from unittest.mock import patch

import boto3
import loguru
import responses
from pytest import fixture
from moto import mock_aws
from mypy_boto3_dynamodb.type_defs import KeySchemaElementTypeDef, AttributeDefinitionTypeDef

from tests import LogCapture, add_test_logging
from tests.carbon_tracking_service.service_tests.infrastructure import config


@fixture(scope='session', autouse=True)
def env_vars():
    with patch.dict('os.environ', config.config):
        yield


@fixture(scope='session')
def logging():
    capture = LogCapture()
    loguru.logger.add(capture.capture_logs)
    return capture

@fixture(scope='session')
def database():
    with mock_aws():
        dynamodb = boto3.resource("dynamodb", region_name=config.config[config.DYNAMO_REGION])
        yield dynamodb.create_table(
            TableName=config.config[config.DYNAMO_TABLE],
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

@fixture
def api_mocks():
  with responses.RequestsMock(assert_all_requests_are_fired=False) as requests_mock:
      yield requests_mock