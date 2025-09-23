from dataclasses import asdict
from datetime import datetime

from assertpy import assert_that

from src.flux_tracking_service.core import TrackedSite
from tests import step, fixture
from tests.flux_tracking_service.features.retrieve_flux_submissions_feature import RetrieveFluxSubmissionsContext


@step
def lambda_is_invoked(ctx: RetrieveFluxSubmissionsContext):
    ctx.lambda_return = ctx.sut({}, {})

@step
def a_tracked_site_is_added_with_last_fetched_LAST_FETCHED(
    ctx: RetrieveFluxSubmissionsContext,
    last_fetched: datetime = None
):
    ctx.submission = fixture.create(str)
    tracked_site = fixture \
        .build(TrackedSite) \
        .with_field(enabled=True) \
        .with_field(last_fetched=last_fetched) \
        .create()
    ctx.station = tracked_site.name
    tracked_site_dict = asdict(tracked_site) | {
        "partition_key": f"TRACKED_SITE#{tracked_site.enabled}",
        "id": f"TRACKED#{tracked_site.name}",
        "last_fetched": tracked_site \
            .last_fetched \
            .isoformat() \
            .replace("+00:00", "Z") \
            if tracked_site.last_fetched else None
    }
    ctx.table.put_item(Item=tracked_site_dict)

@step
def result_is_empty(ctx: RetrieveFluxSubmissionsContext):
    assert_that(ctx.lambda_return).is_not_equal_to({})
    assert_that(ctx.lambda_return["submissions"]).is_empty()