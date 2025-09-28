import boto3
import requests
from boto3.dynamodb.conditions import Key
from icoscp_core.icos import meta
from punq import Container

from src.common.handlers import lazy_handler_factory
from src.common.logging import Logger
from src.flux_tracking_service.core import TrackedSite
from src.flux_tracking_service.ingest.application.commands import FetchNewFluxFilesToProcess
from src.flux_tracking_service.ingest.bootstrap import bootstrap
from src.flux_tracking_service.ingest.crosscutting.mappers import map_core_flux_files_to_responses


def inner_handle(container: Container, _: dict, __: dict) -> dict:
    logger: Logger = container.resolve(Logger)

    with logger.contextualize(operation="ingest"):

        try:
            logger.info("ingestion started")

            fetch_new_files_to_process: FetchNewFluxFilesToProcess = container.resolve(FetchNewFluxFilesToProcess)
            new_files = fetch_new_files_to_process()

            logger.info("ingestion completed")

            return {
                "submissions": map_core_flux_files_to_responses(new_files)
            }
        except Exception as e:
            logger.error(f"ingestion failed: {str(e)}", exc_info=e)
            raise e


handle = lazy_handler_factory(
    inner_handler=inner_handle,
    ioc_registrar=bootstrap
)