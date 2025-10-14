from dataclasses import dataclass

from botocore.exceptions import ClientError

from src.flux_tracking_service.config import DynamoSettings
from src.flux_tracking_service.dynamo import get_table


class SiteNotFoundException(Exception):

    def __init__(self, site: str):
        super().__init__(f"site {site} not found")


class DynamoUpdateSiteLastFetched:
    __slots__ = "table"

    def __init__(self, settings: DynamoSettings):
        self.table = get_table(settings)

    def __call__(self, site: str, submission_timestamp: int) -> None:
        try:
            self.table.update_item(
                Key={
                    "partition_key": "TRACKED_SITE#True",
                    "id": f"TRACKED#{site}"
                },
                UpdateExpression="SET last_fetched = :timestamp",
                ExpressionAttributeValues={":timestamp": submission_timestamp},
                ConditionExpression="attribute_exists(id)",
            )
        except ClientError as e:
            if e.response["Error"]["Code"] == "ConditionalCheckFailedException":
                raise SiteNotFoundException(site)
            raise