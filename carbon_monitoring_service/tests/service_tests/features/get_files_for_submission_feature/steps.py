from typing import Type, cast

from assertpy import assert_that
from boto3.dynamodb.conditions import Key
from mypy_boto3_dynamodb.service_resource import Table
from pytest import fixture
from responses import RequestsMock

from carbon_monitoring_service.src.core import MonitoredSite
from carbon_monitoring_service.src.crosscutting import logging_values
from carbon_monitoring_service.src.entry_points import get_files_for_submission
from lambda_common.handlers import LambdaHandle
from pyight_bdd import BaseBddContext, LogCapture, step, auto_fixture


class GetFilesForSubmissionContext(BaseBddContext):
    sut: LambdaHandle
    requests_mock: RequestsMock
    log_capture: LogCapture
    result: dict
    submission_id: str
    site: str
    table: Table
    submission_timestamp: int
    file_urls: list[str]
    scoped_log_vars: dict
    monitored_site: MonitoredSite

@fixture
def get_files_for_submission_feature(logging, database, api_mocks):
    ctx = GetFilesForSubmissionContext()
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

@step
def lambda_is_invoked(ctx: GetFilesForSubmissionContext):
    ctx.result = ctx.sut({
        "submission_id": ctx.submission_id,
        "site": ctx.site,
        "submission_timestamp": ctx.submission_timestamp
    }, {})

@step
def lambda_should_throw(exception: Type[Exception], ctx: GetFilesForSubmissionContext):
    assert_that(ctx.sut) \
        .raises(exception) \
        .when_called_with({
            "submission_id": ctx.submission_id,
            "site": ctx.site,
            "submission_timestamp": ctx.submission_timestamp
        }, {})

@step
def result_should_be_empty(ctx: GetFilesForSubmissionContext):
    assert_that(ctx.result).is_not_empty()
    assert_that(ctx.result["submissions"]).is_empty()

@step
def result_should_equal_file_url_and_site(ctx: GetFilesForSubmissionContext):
    assert_that(ctx.result).is_not_empty()
    assert_that(ctx.result["submissions"]).is_not_empty()
    assert_that(ctx.result["submissions"]).is_equal_to([
        {"site": ctx.site, "file_url": url}
        for url in ctx.file_urls
    ])

@step
def a_monitored_site_is_added(
    ctx: GetFilesForSubmissionContext
):
    monitored_site = auto_fixture \
        .build(MonitoredSite) \
        .with_field(enabled=True) \
        .create()
    monitored_site_dict = {
        "name": monitored_site.name,
        "last_fetched": monitored_site.last_fetched,
        "partition_key": f"MONITORED_SITE#{monitored_site.enabled}",
        "id": f"MONITORED#{monitored_site.name}"
    }
    ctx.table.put_item(Item=monitored_site_dict)
    ctx.site = monitored_site.name
    ctx.monitored_site = monitored_site

@step
def the_monitored_sites_last_fetched_is_updated(
    ctx: GetFilesForSubmissionContext
):
    response = ctx.table.query(
        KeyConditionExpression=
        Key('partition_key') \
            .eq('MONITORED_SITE#True') & Key('id') \
            .eq(f'MONITORED#{ctx.site}')
    )
    raw_monitored_site = cast(dict, response.get('Items', [])[0])
    monitored_site = MonitoredSite(
        enabled=True,
        last_fetched=raw_monitored_site["last_fetched"],
        name=raw_monitored_site["name"]
    )
    assert_that(monitored_site.last_fetched).is_equal_to(ctx.submission_timestamp)
