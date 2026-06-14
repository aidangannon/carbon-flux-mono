from datetime import datetime
from typing import Type

from assertpy import assert_that
from mypy_boto3_dynamodb.service_resource import Table
from pytest import fixture
from responses import RequestsMock

from carbon_monitoring_service.src.core import MonitoredSite
from carbon_monitoring_service.src.crosscutting import logging_values
from carbon_monitoring_service.src.entry_points import get_latest_submissions
from lambda_common.handlers import LambdaHandle
from pyight_bdd import BaseBddContext, LogCapture, step, auto_fixture
from carbon_monitoring_service.tests.service_tests.infrastructure.api_mocks.icos import (
    Submission,
)


class GetLatestSubmissionsContext(BaseBddContext):
    sut: LambdaHandle
    lambda_return: dict
    table: Table
    log_capture: LogCapture
    requests_mock: RequestsMock
    monitored_sites: list[MonitoredSite]
    submissions: dict[str, Submission]
    scoped_log_vars: dict


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


@step
def lambda_is_invoked(ctx: GetLatestSubmissionsContext):
    ctx.lambda_return = ctx.sut({}, {})


@step
def lambda_should_throw_error(
    ctx: GetLatestSubmissionsContext, exception: Type[Exception]
):
    assert_that(ctx.sut).raises(exception).when_called_with({}, {})


@step
def site_created_with_last_fetched_FETCHED(
    ctx: GetLatestSubmissionsContext,
    fetched: datetime | None = None
):
    monitored_site = (
        auto_fixture.build(MonitoredSite)
        .with_field(enabled=True)
        .with_field(last_fetched=fetched)
        .create()
    )
    monitored_site_dict = {
        "name": monitored_site.name,
        "last_fetched": int(fetched.timestamp()) if fetched else None,
        "partition_key": f"MONITORED_SITE#{monitored_site.enabled}",
        "id": f"MONITORED#{monitored_site.name}",
    }
    ctx.table.put_item(Item=monitored_site_dict)
    ctx.monitored_sites.append(monitored_site)


@step
def submission_created_for_site_SITE(
    site: str,
    submission_time: datetime,
    ctx: GetLatestSubmissionsContext
):
    submission = auto_fixture.create(str)
    ctx.submissions[site] = Submission(submission, submission_time)


@step
def result_should_be_empty(ctx: GetLatestSubmissionsContext):
    assert_that(ctx.lambda_return).is_not_equal_to({})
    assert_that(ctx.lambda_return["submissions"]).is_empty()


@step
def result_should_have_submissions_SUBS(
    subs: dict[str, Submission],
    ctx: GetLatestSubmissionsContext
):
    expected_submissions = [
        {
            "site": monitored_site,
            "submission": submission.id,
            "submission_time": int(submission.submission_time.timestamp()),
        }
        for monitored_site, submission in subs.items()
    ]
    assert_that(ctx.lambda_return).is_not_equal_to({})
    assert_that(ctx.lambda_return["submissions"]).is_not_empty()
    assert_that(ctx.lambda_return["submissions"]).contains(*expected_submissions)
