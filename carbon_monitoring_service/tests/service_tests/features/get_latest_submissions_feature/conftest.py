from pytest import fixture

from carbon_monitoring_service.src.crosscutting import logging_values
from carbon_monitoring_service.src.entry_points import get_latest_submissions
from carbon_monitoring_service.tests.service_tests.features.get_latest_submissions_feature import GetLatestSubmissionsContext


@fixture
def get_latest_submissions_feature(logging, database, api_mocks):
    ctx = GetLatestSubmissionsContext()
    ctx.table = database
    ctx.sut = get_latest_submissions.handle
    ctx.requests_mock = api_mocks
    ctx.log_capture = logging
    ctx.monitored_sites = []
    ctx.submissions = {}
    ctx.scoped_log_vars = {logging_values.OPERATION: logging_values.DETECT_SUBMISSIONS}
    return ctx
