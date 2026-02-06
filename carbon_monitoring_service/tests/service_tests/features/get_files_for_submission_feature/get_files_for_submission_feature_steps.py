from typing import Type

from assertpy import assert_that
from boto3.dynamodb.conditions import Key

from carbon_monitoring_service.src.core import MonitoredSite
from pyight_bdd import step, auto_fixture
from carbon_monitoring_service.tests.service_tests.features.get_files_for_submission_feature import \
    ResolveFluxSubmissionContext


@step
def lambda_is_invoked(ctx: ResolveFluxSubmissionContext):
    ctx.result = ctx.sut({
        "submission_id": ctx.submission_id,
        "site": ctx.site,
        "submission_timestamp": ctx.submission_timestamp
    }, {})

@step
def lambda_should_throw(exception: Type[Exception], ctx: ResolveFluxSubmissionContext):
    assert_that(ctx.sut) \
        .raises(exception) \
        .when_called_with({
            "submission_id": ctx.submission_id,
            "site": ctx.site,
            "submission_timestamp": ctx.submission_timestamp
        }, {})

@step
def result_should_be_empty(ctx: ResolveFluxSubmissionContext):
    assert_that(ctx.result).is_not_empty()
    assert_that(ctx.result["submissions"]).is_empty()

@step
def result_should_equal_file_url_and_site(ctx: ResolveFluxSubmissionContext):
    assert_that(ctx.result).is_not_empty()
    assert_that(ctx.result["submissions"]).is_not_empty()
    assert_that(ctx.result["submissions"]).is_equal_to([
        {"site": ctx.site, "file_url": url}
        for url in ctx.file_urls
    ])

@step
def a_monitored_site_is_added(
    ctx: ResolveFluxSubmissionContext
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
    ctx: ResolveFluxSubmissionContext
):
    response = ctx.table.query(
        KeyConditionExpression=
        Key('partition_key') \
            .eq('MONITORED_SITE#True') & Key('id') \
            .eq(f'MONITORED#{ctx.site}')
    )
    raw_monitored_site = response.get('Items', [])[0]
    monitored_site = MonitoredSite(
        enabled=True,
        last_fetched=raw_monitored_site["last_fetched"],
        name=raw_monitored_site["name"]
    )
    assert_that(monitored_site.last_fetched).is_equal_to(ctx.submission_timestamp)
