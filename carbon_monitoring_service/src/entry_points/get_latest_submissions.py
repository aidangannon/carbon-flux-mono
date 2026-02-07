from lambda_common import logging
import carbon_monitoring_service.src.bootstrapping as bootstrapping
import carbon_monitoring_service.src.application.slices.get_latest_submissions as get_latest_submissions
import carbon_monitoring_service.src.crosscutting.logging_values as logging_values


bootstrapping.configure_adapters()

def handle(_: dict, __: dict) -> dict:
    with logging.logger.contextualize(**{logging_values.OPERATION: logging_values.DETECT_SUBMISSIONS}):

        try:
            logging.logger.info("handler started")

            flux_submissions = get_latest_submissions.get()

            logging.logger.info("handler completed")

            flux_submissions_to_return = [
                {
                    "site": flux_submission.site,
                    "submission": flux_submission.submission,
                    "submission_time": flux_submission.submission_time
                }
                for flux_submission in flux_submissions
            ]

            return {
                "submissions": flux_submissions_to_return
            }
        except Exception as e:
            logging.logger.error(f"handler failed: {str(e)}", exc_info=e)
            raise e
