import boto3
import responses
from moto import mock_aws
from mypy_boto3_dynamodb.type_defs import KeySchemaElementTypeDef, AttributeDefinitionTypeDef

from tests.flux_tracking_service.service_tests.infrastructure import config

# register all fixtures from submodule here
from tests.flux_tracking_service.service_tests.infrastructure.lambda_config.flux_submission_detector.fixtures import *


@fixture(scope='session')
def database():
    with mock_aws():
        dynamodb = boto3.resource('dynamodb', region_name=config.AWS_REGION)
        yield dynamodb.create_table(
            TableName=config.DYNAMO_DB_TABLE,
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