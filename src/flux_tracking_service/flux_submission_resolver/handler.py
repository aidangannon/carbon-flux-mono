from punq import Container

from src.common.handlers import lazy_handler_factory
from src.common.ioc import resolve_service
from src.common.logging import Logger
from src.flux_tracking_service.core import OPERATION, RESOLVE_SUBMISSIONS
from src.flux_tracking_service.flux_submission_resolver.application import ResolveFilesForSubmission
from src.flux_tracking_service.flux_submission_resolver.bootstrap import bootstrap


def inner_handle(container: Container, event: dict, __: dict) -> dict:
    logger = resolve_service(container, Logger)

    with logger.contextualize(**{OPERATION: RESOLVE_SUBMISSIONS}):

        try:
            logger.info("handler started")

            resolve_files_for_submission = resolve_service(container, ResolveFilesForSubmission)
            resolve_files_for_submission(event["site"], event["submission_id"], event["submission_timestamp"])

            logger.info("handler completed")

            return {
                "submissions": []
            }
        except Exception as e:
            logger.error(f"handler failed: {str(e)}", exc_info=e)
            raise e



handle = lazy_handler_factory(
    inner_handler=inner_handle,
    ioc_registrar=bootstrap
)