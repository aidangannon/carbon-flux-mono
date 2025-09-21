from tests import scenario
from tests.flux_tracking_service.features.retrieve_flux_submissions_feature.retrieve_flux_submissions_feature_steps import \
    lambda_is_invoked, result_is_empty


@scenario
def test_when_no_data_is_present_in_db_the_lambda_should_return_empty_list(retrieve_flux_submissions_feature):
    ctx = retrieve_flux_submissions_feature
    ctx.runner \
        .when(lambda_is_invoked(ctx)) \
        .then(result_is_empty(ctx)) \
        .run()