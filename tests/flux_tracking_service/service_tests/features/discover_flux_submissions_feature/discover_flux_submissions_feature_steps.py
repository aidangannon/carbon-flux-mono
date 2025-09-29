from datetime import datetime
from typing import Optional, Type

from assertpy import assert_that

from src.flux_tracking_service.core import TrackedSite
from tests import step, fixture
from tests.flux_tracking_service.service_tests.features.discover_flux_submissions_feature import DiscoverFluxSubmissionsContext
from tests.flux_tracking_service.service_tests.infrastructure.api_mocks.icos import Submission


@step
def lambda_is_invoked(ctx: DiscoverFluxSubmissionsContext):
    ctx.lambda_return = ctx.sut({}, {})

@step
def lambda_should_throw_error(
    ctx: DiscoverFluxSubmissionsContext,
    exception: Type[Exception]
):
    assert_that(ctx.sut).raises(exception).when_called_with({}, {})

@step
def a_tracked_site_is_added_with_last_fetched_LAST_FETCHED(
    ctx: DiscoverFluxSubmissionsContext,
    last_fetched: Optional[datetime] = None
):
    tracked_site = fixture \
        .build(TrackedSite) \
        .with_field(enabled=True) \
        .with_field(last_fetched=last_fetched) \
        .create()
    tracked_site_dict = {
        "name": tracked_site.name,
        "last_fetched": int(last_fetched.timestamp()) if last_fetched else None,
        "partition_key": f"TRACKED_SITE#{tracked_site.enabled}",
        "id": f"TRACKED#{tracked_site.name}"
    }
    ctx.table.put_item(Item=tracked_site_dict)
    ctx.tracked_sites.append(tracked_site)

@step
def a_submission_exists_for_tracked_site_TRACKED_SITE(
    tracked_site: str,
    submission_time: datetime,
    ctx: DiscoverFluxSubmissionsContext
):
    submission = fixture.create(str)
    ctx.submissions[tracked_site] = Submission(submission, submission_time)

@step
def result_is_empty(ctx: DiscoverFluxSubmissionsContext):
    assert_that(ctx.lambda_return).is_not_equal_to({})
    assert_that(ctx.lambda_return["submissions"]).is_empty()

@step
def result_has_submissions_SUBMISSIONS_for_tracked_sites(
    submissions: dict[str, Submission],
    ctx: DiscoverFluxSubmissionsContext
):
    expected_submissions = [
        {
            "site": tracked_site,
            "submission": submission.id,
            "submission_time": int(submission.submission_time.timestamp())
        }
    for tracked_site, submission in submissions.items()]
    assert_that(ctx.lambda_return).is_not_equal_to({})
    assert_that(ctx.lambda_return["submissions"]).is_not_empty()
    assert_that(ctx.lambda_return["submissions"]).contains(*expected_submissions)