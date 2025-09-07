import boto3
from moto import mock_aws
from pytest import fixture

@fixture(scope='session', autouse=True)
def setup_database():
    with mock_aws():
        dynamodb = boto3.resource('dynamodb')
        dynamodb.create_table(
            TableName='fluxter-db',
            KeySchema=[
                {'AttributeName': 'partition_key', 'KeyType': 'HASH'},
                {'AttributeName': 'id', 'KeyType': 'RANGE'}
            ],
            AttributeDefinitions=[
                {'AttributeName': 'partition_key', 'AttributeType': 'S'},
                {'AttributeName': 'id', 'AttributeType': 'S'}
            ],
            BillingMode='PAY_PER_REQUEST'
        )
        yield