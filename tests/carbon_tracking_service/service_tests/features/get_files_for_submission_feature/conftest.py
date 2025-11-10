from pytest import fixture

import tests
from src.carbon_tracking_service.core import RESOLVE_SUBMISSIONS, OPERATION
from tests.carbon_tracking_service.service_tests.features.get_files_for_submission_feature import \
    ResolveFluxSubmissionContext


@fixture
def resolve_flux_submission_feature(flux_submission_resolver_handler, flux_submission_resolver_container, database, api_mocks):
    ctx = ResolveFluxSubmissionContext()
    ctx.table = database
    ctx.sut = flux_submission_resolver_handler
    ctx.requests_mock = api_mocks
    ctx.container = flux_submission_resolver_container
    ctx.submission_id = tests.fixture.create(str)
    ctx.site = tests.fixture.create(str)
    ctx.file_urls = tests.fixture.create_many(str)
    ctx.submission_timestamp = tests.fixture.create_many(int)
    ctx.scoped_log_vars = {OPERATION: RESOLVE_SUBMISSIONS}
    return ctx