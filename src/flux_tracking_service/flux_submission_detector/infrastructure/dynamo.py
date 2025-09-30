from boto3.dynamodb.conditions import Key

from src.flux_tracking_service.core import TrackedSite
from src.flux_tracking_service.dynamo import get_table
from src.flux_tracking_service.config import DynamoSettings
from src.flux_tracking_service.flux_submission_detector.mappers import map_data_tracked_sites_to_core_tracked_sites


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

        return map_data_tracked_sites_to_core_tracked_sites(items)