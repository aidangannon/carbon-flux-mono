from lambda_common import logging
from carbon_tracking_service.src import bootstrapping
from carbon_tracking_service.src.application import ports
from carbon_tracking_service.src.application.slices import get_files_for_submission
from carbon_tracking_service.src.crosscutting import logging_values


def handle(event: dict, _: dict) -> dict:
    with logging.logger.contextualize(**{logging_values.OPERATION: logging_values.RESOLVE_SUBMISSIONS}):

        try:
            logging.logger.info("handler started")

            files = get_files_for_submission.execute(
                site=event["site"],
                submission=event["submission_id"],
                submission_timestamp=event["submission_timestamp"],
                facade=bootstrapping.container[ports.SubmissionsFacade]
            )

            logging.logger.info("handler completed")

            return {
                "submissions": [
                    {
                        "site": event["site"],
                        "file_url": file
                    }
                    for file in files
                ]
            }
        except Exception as e:
            logging.logger.error(f"handler failed: {str(e)}", exc_info=e)
            raise e
