from pytest import fixture

from tests.flux_tracking_service.service_tests.features.retrieve_flux_submissions_feature import RetrieveFluxSubmissionsContext


@fixture
def retrieve_flux_submissions_feature(flux_submission_detector_handler, flux_submission_detector_container, database, api_mocks):
    ctx = RetrieveFluxSubmissionsContext()
    ctx.table = database
    ctx.sut = flux_submission_detector_handler
    ctx.requests_mock = api_mocks
    ctx.container = flux_submission_detector_container
    ctx.tracked_sites = []
    ctx.submissions = {}
    ctx.scoped_log_vars = {"operation": "flux_submission_detector"}
    return ctx