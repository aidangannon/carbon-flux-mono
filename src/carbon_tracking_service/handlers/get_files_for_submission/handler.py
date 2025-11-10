from src.common import logging
from src.carbon_tracking_service import bootstrapping
from src.carbon_tracking_service.application import ports
from src.carbon_tracking_service.application.slices import get_files_for_submission
from src.carbon_tracking_service.crosscutting import logging_values


def handle(event: dict, _: dict) -> dict:
    with logging.logger.contextualize(**{logging_values.OPERATION: logging_values.RESOLVE_SUBMISSIONS}):

        try:
            logging.logger.info("handler started")

            files = get_files_for_submission.execute(
                site=event["site"],
                submission=event["submission_id"],
                submission_timestamp=event["submission_timestamp"],
                submission_client=bootstrapping.container[ports.FluxClient],
                tracked_site_repo=bootstrapping.container[ports.TrackedSiteRepository]
            )

            logging.logger.info("handler completed")

            return {
                "submissions": []
            }
        except Exception as e:
            logging.logger.error(f"handler failed: {str(e)}", exc_info=e)
            raise e