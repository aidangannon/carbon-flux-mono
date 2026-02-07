from pytest import fixture

import carbon_monitoring_service.src.crosscutting.logging_values as logging_values
import carbon_monitoring_service.src.entry_points.get_files_for_submission as get_files_for_submission
from pyight_bdd import auto_fixture
from carbon_monitoring_service.tests.service_tests.features.get_files_for_submission_feature import \
    ResolveFluxSubmissionContext


@fixture
def get_files_for_submission_feature(logging, database, api_mocks):
    ctx = ResolveFluxSubmissionContext()
    ctx.table = database
    ctx.log_capture = logging
    ctx.requests_mock = api_mocks
    ctx.sut = get_files_for_submission.handle
    ctx.submission_id = auto_fixture.create(str)
    ctx.site = auto_fixture.create(str)
    ctx.file_urls = auto_fixture.create_many(str)
    ctx.submission_timestamp = auto_fixture.create(int)
    ctx.scoped_log_vars = {logging_values.OPERATION: logging_values.RESOLVE_SUBMISSIONS}
    return ctx
