from src.common import logging
from src.carbon_tracking_service import bootstrapping
from src.carbon_tracking_service.application import ports
from src.carbon_tracking_service.application.slices import get_latest_submissions
from src.carbon_tracking_service.crosscutting import logging_values


def handle(_: dict, __: dict) -> dict:
    with logging.logger.contextualize(**{logging_values.OPERATION: logging_values.DETECT_SUBMISSIONS}):

        try:
            logging.logger.info("handler started")

            flux_submissions = get_latest_submissions.execute(bootstrapping.container[ports.SubmissionsFacade])

            logging.logger.info("handler completed")

            return {
                "submissions": [
                    {
                        "site": flux_submission.site,
                        "submission": flux_submission.submission,
                        "submission_time": flux_submission.submission_time
                    }
                    for flux_submission in flux_submissions
                ]
            }
        except Exception as e:
            logging.logger.error(f"handler failed: {str(e)}", exc_info=e)
            raise e