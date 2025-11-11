from pytest import fixture

from src.carbon_tracking_service.entry_points.get_files_for_submission import handler
from src.carbon_tracking_service.crosscutting import logging_values
from tests import auto_fixture
from tests.carbon_tracking_service.service_tests.features.get_files_for_submission_feature import \
    ResolveFluxSubmissionContext


@fixture
def get_files_for_submission_feature(logging, database, api_mocks):
    ctx = ResolveFluxSubmissionContext()
    ctx.table = database
    ctx.log_capture = logging
    ctx.requests_mock = api_mocks
    ctx.sut = handler.handle
    ctx.submission_id = auto_fixture.create(str)
    ctx.site = auto_fixture.create(str)
    ctx.file_urls = auto_fixture.create_many(str)
    ctx.submission_timestamp = auto_fixture.create_many(int)
    ctx.scoped_log_vars = {logging_values.OPERATION: logging_values.RESOLVE_SUBMISSIONS}
    return ctx