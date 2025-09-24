from datetime import datetime, timezone

import boto3
import requests
from boto3.dynamodb.conditions import Key
from dacite import from_dict
from dacite.data import Data
from icoscp_core.icos import meta
from punq import Container

from src.common.handlers import lazy_handler_factory
from src.common.logging import Logger
from src.flux_tracking_service.core import TrackedSite
from src.flux_tracking_service.ingest.bootstrap import bootstrap


def inner_handle(
    container: Container,
    event: dict,
    context: dict
) -> dict:
    logger: Logger = container.resolve(Logger)

    table = boto3.resource('dynamodb', region_name="eu-west-2").Table('flux-tracking-db')
    response = table.query(
        KeyConditionExpression=
            Key('partition_key') \
                .eq('TRACKED_SITE#True') & Key('id') \
                .begins_with('TRACKED')
    )
    items = response.get('Items', [])
    submissions = []

    for item in items:
        tracked_site = TrackedSite(
            name=item["name"],
            enabled=item["enabled"],
            last_fetched=int(item["last_fetched"]) if item["last_fetched"] else None
        )
        response_from_icos = meta.list_data_objects(
            datatype='http://meta.icos-cp.eu/resources/cpmeta/etcEddyFluxRawSeriesCsv',
            station=f'http://meta.icos-cp.eu/resources/stations/{tracked_site.name}',
            order_by={"prop": "timeEnd", "descending": True},
            limit=1
        )

        if len(response_from_icos) == 0:
            logger.error(f"no submissions found for {tracked_site.name}")
            continue

        submission = response_from_icos[0]

        if tracked_site.last_fetched is not None and int(submission.submission_time.timestamp()) <= tracked_site.last_fetched:
            logger.warning(f"no new submissions for {tracked_site.name}")
            continue

        content_response = requests.get(f"https://data.icos-cp.eu/zip/{submission.uri.split('/')[4]}/listContents")
        json_files = content_response.json()
        paths = [file["path"] for file in json_files]

        submissions.extend([{"site": tracked_site.name, "file_url": path} for path in paths])

    return {
        "submissions": submissions
    }

handle = lazy_handler_factory(
    inner_handler=inner_handle,
    ioc_registrar=bootstrap
)