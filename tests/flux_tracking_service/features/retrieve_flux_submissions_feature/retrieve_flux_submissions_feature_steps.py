from dataclasses import asdict
from datetime import datetime
from typing import Optional, Union

from assertpy import assert_that

from src.flux_tracking_service.core import TrackedSite
from src.flux_tracking_service.ingest.core import Submission
from tests import step, fixture
from tests.flux_tracking_service.features.retrieve_flux_submissions_feature import RetrieveFluxSubmissionsContext


@step
def lambda_is_invoked(ctx: RetrieveFluxSubmissionsContext):
    ctx.lambda_return = ctx.sut({}, {})

@step
def a_tracked_site_is_added_with_last_fetched_LAST_FETCHED(
    ctx: RetrieveFluxSubmissionsContext,
    last_fetched: Optional[datetime] = None
):
    tracked_site = fixture \
        .build(TrackedSite) \
        .with_field(enabled=True) \
        .with_field(last_fetched=last_fetched) \
        .create()
    ctx.station = tracked_site.name
    tracked_site_dict = {
        "name": tracked_site.name,
        "enabled": tracked_site.enabled,
        "last_fetched": int(last_fetched.timestamp()) if last_fetched else None,
        "partition_key": f"TRACKED_SITE#{tracked_site.enabled}",
        "id": f"TRACKED#{tracked_site.name}"
    }
    ctx.table.put_item(Item=tracked_site_dict)
    ctx.tracked_sites.append(tracked_site)

@step
def a_submission_exists_for_tracked_site_TRACKED_SITE(
    tracked_site: str,
    ctx: RetrieveFluxSubmissionsContext
):
    submission = Submission(
        submission_id=fixture.create(str),
        file_urls=fixture.create_many(str)
    )
    ctx.submission_contents[tracked_site] = submission

@step
def result_is_empty(ctx: RetrieveFluxSubmissionsContext):
    assert_that(ctx.lambda_return).is_not_equal_to({})
    assert_that(ctx.lambda_return["submissions"]).is_empty()

@step
def result_has_submissions_SUBMISSIONS_for_tracked_site_TRACKED_SITE(
    submissions: list,
    tracked_site: str,
    ctx: RetrieveFluxSubmissionsContext
):
    assert_that(ctx.lambda_return).is_not_equal_to({})
    assert_that(ctx.lambda_return["submissions"]).is_not_empty()
    assert_that(ctx.lambda_return["submissions"]).contains({
        "site": tracked_site,
        "submissions": submissions
    })