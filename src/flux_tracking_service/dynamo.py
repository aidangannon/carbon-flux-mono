import boto3
from mypy_boto3_dynamodb.service_resource import Table

from src.flux_tracking_service.config import DynamoSettings


def get_table(settings: DynamoSettings) -> Table:
    return boto3 \
        .resource('dynamodb', region_name=settings.region) \
        .Table(name=settings.table_name)