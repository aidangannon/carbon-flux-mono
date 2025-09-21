from assertpy import assert_that

from tests import step
from tests.flux_tracking_service.features.retrieve_flux_submissions_feature import RetrieveFluxSubmissionsContext


@step
def lambda_is_invoked(context: RetrieveFluxSubmissionsContext):
    context.lambda_return = context.sut({}, {})

@step
def result_is_empty(context: RetrieveFluxSubmissionsContext):
    assert_that(context.lambda_return).is_not_equal_to({})
    assert_that(context.lambda_return["submissions"]).is_empty()