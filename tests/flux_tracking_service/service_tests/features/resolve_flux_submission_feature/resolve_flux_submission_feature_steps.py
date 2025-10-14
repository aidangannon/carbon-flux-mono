from typing import Type

from assertpy import assert_that

from src.flux_tracking_service.core import TrackedSite
from tests import step, fixture
from tests.flux_tracking_service.service_tests.features.resolve_flux_submission_feature import \
    ResolveFluxSubmissionContext


@step
def lambda_is_invoked_with_submission_id_SUBMISSION_ID_and_site_SITE(
    site: str,
    submission_id: str,
    submission_timestamp: int,
    ctx: ResolveFluxSubmissionContext
):
    ctx.result = ctx.sut({
        "submission_id": submission_id,
        "site": site,
        "submission_timestamp": submission_timestamp
    }, {})

@step
def lambda_should_throw_with_submission_id_SUBMISSION_ID_and_site_SITE(
    site: str,
    submission_id: str,
    submission_timestamp: str,
    exception: Type[Exception],
    ctx: ResolveFluxSubmissionContext
):
    assert_that(ctx.sut) \
        .raises(exception) \
        .when_called_with({
            "submission_id": submission_id,
            "site": site,
            "submission_timestamp": submission_timestamp
        }, {})

@step
def result_should_be_empty(ctx: ResolveFluxSubmissionContext):
    assert_that(ctx.result).is_not_empty()
    assert_that(ctx.result["submissions"]).is_empty()

@step
def a_tracked_site_is_added_with_last_fetched_LAST_FETCHED(
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
    ctx.tracked_site = tracked_site