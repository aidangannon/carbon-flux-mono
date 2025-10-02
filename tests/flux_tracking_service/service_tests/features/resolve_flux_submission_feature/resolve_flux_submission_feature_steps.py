from typing import Type

from assertpy import assert_that

from tests import step
from tests.flux_tracking_service.service_tests.features.resolve_flux_submission_feature import \
    ResolveFluxSubmissionContext


@step
def lambda_is_invoked_with_submission_id_SUBMISSION_ID_and_site_SITE(
    submission_id: str,
    site: str,
    ctx: ResolveFluxSubmissionContext
):
    ctx.result = ctx.sut({"submission_id": submission_id, "site": site}, {})

@step
def lambda_should_throw_with_submission_id_SUBMISSION_ID_and_site_SITE(
    submission_id: str,
    site: str,
    exception: Type[Exception],
    ctx: ResolveFluxSubmissionContext
):
    assert_that(ctx.sut) \
        .raises(exception) \
        .when_called_with({"submission_id": submission_id, "site": site}, {})

@step
def result_should_be_empty(ctx: ResolveFluxSubmissionContext):
    assert_that(ctx.result).is_not_empty()
    assert_that(ctx.result["submissions"]).is_empty()