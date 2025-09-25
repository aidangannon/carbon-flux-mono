from dataclasses import dataclass

import boto3
from boto3.dynamodb.conditions import Key
from mypy_boto3_dynamodb.service_resource import Table

from src.flux_tracking_service.core import TrackedSite
from src.flux_tracking_service.dynamo import get_table
from src.flux_tracking_service.config import DynamoSettings


class DynamoGetAllTrackedSites:
    __slots__ = "table"

    def __init__(self, dynamo_settings: DynamoSettings):
        self.table = get_table(dynamo_settings)

    def __call__(self) -> list[TrackedSite]:
        response = self.table.query(
            KeyConditionExpression=
            Key('partition_key') \
                .eq('TRACKED_SITE#True') & Key('id') \
                .begins_with('TRACKED')
        )
        items = response.get('Items', [])

        return [TrackedSite(
            name=item["name"],
            last_fetched=int(item["last_fetched"]) if item["last_fetched"] else None,
            enabled=item["enabled"]
        ) for item in items]