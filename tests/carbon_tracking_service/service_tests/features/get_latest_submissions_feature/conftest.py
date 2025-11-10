from pytest import fixture

from src.carbon_tracking_service.crosscutting import logging_values
from tests.carbon_tracking_service.service_tests.features.get_latest_submissions_feature import DiscoverFluxSubmissionsContext


@fixture
def get_latest_submissions_feature(flux_submission_detector_handler, flux_submission_detector_container, database, api_mocks):
    ctx = DiscoverFluxSubmissionsContext()
    ctx.table = database
    ctx.sut = flux_submission_detector_handler
    ctx.requests_mock = api_mocks
    ctx.container = flux_submission_detector_container
    ctx.tracked_sites = []
    ctx.submissions = {}
    ctx.scoped_log_vars = {logging_values.OPERATION: logging_values.DETECT_SUBMISSIONS}
    return ctx