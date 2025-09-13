import boto3
from moto import mock_aws
from mypy_boto3_dynamodb.type_defs import KeySchemaElementTypeDef, AttributeDefinitionTypeDef
from punq import Container
from pytest import fixture

from src.fluxter.fluxter_scrape import bootstrap
from src.fluxter.fluxter_scrape import inner_handle
from tests import add_test_logging


@fixture(scope='session')
def database():
    import os
    os.environ['AWS_DEFAULT_REGION'] = 'eu-west-2'
    os.environ['AWS_ACCESS_KEY_ID'] = 'testing'
    os.environ['AWS_SECRET_ACCESS_KEY'] = 'testing'
    print(f"AWS Region: {os.environ.get('AWS_DEFAULT_REGION', 'not set')}")
    print(f"Running in CI: {os.environ.get('CI', 'false')}")
    with mock_aws():
        dynamodb = boto3.resource('dynamodb', region_name='eu-west-2')
        yield dynamodb.create_table(
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