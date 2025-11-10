from typing import Type

from assertpy import assert_that
from boto3.dynamodb.conditions import Key

from src.carbon_tracking_service.core import TrackedSite
from tests import step, fixture
from tests.carbon_tracking_service.service_tests.features.get_files_for_submission_feature import \
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
def result_should_contain_map_file_url_and_site(ctx: ResolveFluxSubmissionContext):
    assert_that(ctx.result).is_not_empty()
    assert_that(ctx.result["submissions"]).is_not_empty()
    assert_that(ctx.result["submissions"]).contains([
        {"site": ctx.site, "file_url": url}
        for url in ctx.file_urls
    ])

@step
def a_tracked_site_is_added(
    ctx: ResolveFluxSubmissionContext
):
    tracked_site = fixture \
        .build(TrackedSite) \
        .with_field(enabled=True) \
        .create()
    tracked_site_dict = {
        "name": tracked_site.name,
        "last_fetched": tracked_site.last_fetched,
        "partition_key": f"TRACKED_SITE#{tracked_site.enabled}",
        "id": f"TRACKED#{tracked_site.name}"
    }
    ctx.table.put_item(Item=tracked_site_dict)
    ctx.site = tracked_site.name
    ctx.tracked_site = tracked_site

@step
def the_tracked_sites_last_fetched_is_updated(
    ctx: ResolveFluxSubmissionContext
):
    response = ctx.table.query(
        KeyConditionExpression=
        Key('partition_key') \
            .eq('TRACKED_SITE#True') & Key('id') \
            .begins_with('TRACKED')
    )
    raw_tracked_site = response.get('Items', [])[0]
    tracked_site = TrackedSite(
        enabled=True,
        last_fetched=raw_tracked_site["last_fetched"],
        name=raw_tracked_site["name"]
    )
    assert_that(tracked_site.last_fetched).is_equal_to(ctx.submission_timestamp)