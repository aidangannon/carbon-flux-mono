from punq import Container

from src.common.handlers import lazy_handler_factory
from src.common.ioc import resolve_service
from src.common.logging import Logger
from src.flux_tracking_service.core import DETECT_SUBMISSIONS, OPERATION
from src.flux_tracking_service.flux_submission_detector.application import FetchNewFluxFilesToProcess
from src.flux_tracking_service.flux_submission_detector.bootstrap import bootstrap
from src.flux_tracking_service.flux_submission_detector.mappers import map_core_flux_submissions_to_responses


def inner_handle(container: Container, _: dict, __: dict) -> dict:
    logger: Logger = resolve_service(container, Logger)

    with logger.contextualize(**{OPERATION: DETECT_SUBMISSIONS}):

        try:
            logger.info("handler started")

            fetch_new_files_to_process = resolve_service(container, FetchNewFluxFilesToProcess)
            new_files = fetch_new_files_to_process()

            logger.info("handler completed")

            return {
                "submissions": map_core_flux_submissions_to_responses(new_files)
            }
        except Exception as e:
            logger.error(f"handler failed: {str(e)}", exc_info=e)
            raise e


handle = lazy_handler_factory(
    inner_handler=inner_handle,
    ioc_registrar=bootstrap
)