from assertpy import assert_that

from tests import step
from tests.flux_tracking_service.service_tests.features.resolve_flux_submission_feature import \
    ResolveFluxSubmissionContext


@step
def lambda_is_invoked(ctx: ResolveFluxSubmissionContext):
    ctx.sut({}, {})

@step
def lambda_is_invoked(ctx: ResolveFluxSubmissionContext):
    ctx.result = ctx.sut({}, {})

@step
def result_should_be_empty(ctx: ResolveFluxSubmissionContext):
    assert_that(ctx.result).is_not_empty()
    assert_that(ctx.result["file_urls"]).is_empty()