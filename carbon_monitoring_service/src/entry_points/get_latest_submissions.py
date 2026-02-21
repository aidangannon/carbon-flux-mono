from lambda_common import logging
from carbon_monitoring_service.src import bootstrapping
from carbon_monitoring_service.src.application.slices import get_latest_submissions
from carbon_monitoring_service.src.crosscutting import logging_values


bootstrapping.configure_adapters()


def handle(event: dict, context: dict) -> dict:
    with logging.logger.contextualize(**{
        logging_values.OPERATION: logging_values.DETECT_SUBMISSIONS
    }):
        try:
            logging.logger.info("handler started")

            flux_submissions = get_latest_submissions.get()

            logging.logger.info("handler completed")

            flux_submissions_to_return = [
                {
                    "site": flux_submission.site,
                    "submission": flux_submission.submission,
                    "submission_time": flux_submission.submission_time,
                }
                for flux_submission in flux_submissions
            ]

            return {"submissions": flux_submissions_to_return}
        except Exception as e:
            logging.logger.error(f"handler failed: {str(e)}", exc_info=e)
            raise e
