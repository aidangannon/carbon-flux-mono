import boto3
from boto3.dynamodb.conditions import Key
from dacite import from_dict
from icoscp_core.icos import meta
from punq import Container

from src.common.handlers import lazy_handler_factory
from src.flux_tracking_service.core import TrackedSite
from src.flux_tracking_service.ingest.bootstrap import bootstrap


def inner_handle(
    container: Container,
    event: dict,
    context: dict
) -> dict:
    table = boto3.resource('dynamodb').Table('flux-tracking-db')
    response = table.query(
        KeyConditionExpression=
            Key('partition_key') \
                .eq('TRACKED_SITE#True') & Key('id') \
                .begins_with('TRACKED')
    )
    first_item = next(iter(response.get('Items', [])), None)
    if first_item is None:
        return {
            "submissions": []
        }

    tracked_site = from_dict(TrackedSite, first_item)
    response_from_icos = meta.list_data_objects(
        datatype='http://meta.icos-cp.eu/resources/cpmeta/etcEddyFluxRawSeriesCsv',
        station=f'http://meta.icos-cp.eu/resources/stations/{tracked_site.name}',
        order_by={"prop": "timeEnd", "descending": True},
        limit=1
    )

    return {
        "submissions": []
    }

handle = lazy_handler_factory(
    inner_handler=inner_handle,
    ioc_registrar=bootstrap
)