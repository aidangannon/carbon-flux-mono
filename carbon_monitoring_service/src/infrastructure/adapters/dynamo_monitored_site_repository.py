from mypy_boto3_dynamodb.service_resource import Table
import functools

import boto3
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError

from carbon_monitoring_service.src.core import MonitoredSite
from carbon_monitoring_service.src.crosscutting import config

from carbon_monitoring_service.src.application.exceptions import SiteNotFoundException

__all__ = ["get_all", "update_last_fetched"]


@functools.lru_cache(maxsize=1)
def lazy_table() -> Table:
    return boto3 \
        .resource('dynamodb', region_name=config.lazy_dynamo_settings().region) \
        .Table(name=config.lazy_dynamo_settings().table_name)


def get_all() -> list[MonitoredSite]:
    response = lazy_table().query(
        KeyConditionExpression=
            Key('partition_key') \
                .eq('MONITORED_SITE#True') & Key('id') \
                .begins_with('MONITORED')
        )
    items = response.get('Items', [])

    return [
        MonitoredSite(
            name=site["name"],
            last_fetched=int(site["last_fetched"]) if site["last_fetched"] else None,
            enabled=True
        )
        for site in items
    ]


def update_last_fetched(site: str, submission_timestamp: int) -> None:
    try:
        lazy_table().update_item(
            Key={
                "partition_key": "MONITORED_SITE#True",
                "id": f"MONITORED#{site}"
            },
            UpdateExpression="SET last_fetched = :timestamp",
            ExpressionAttributeValues={":timestamp": submission_timestamp},
            ConditionExpression="attribute_exists(id)",
        )
    except ClientError as e:
        if e.response["Error"]["Code"] == "ConditionalCheckFailedException":
            raise SiteNotFoundException(site)
        raise
