from pytest import fixture

import tests
from tests.flux_tracking_service.service_tests.features.discover_flux_submissions_feature import \
    DiscoverFluxSubmissionsContext


@fixture
def resolve_flux_submission_feature(flux_submission_detector_handler, flux_submission_detector_container, database, api_mocks):
    ctx = DiscoverFluxSubmissionsContext()
    ctx.table = database
    ctx.sut = flux_submission_detector_handler
    ctx.requests_mock = api_mocks
    ctx.container = flux_submission_detector_container
    ctx.submission_id = tests.fixture.create(str)
    ctx.scoped_log_vars = {"operation": "flux_submission_resolver"}
    return ctx