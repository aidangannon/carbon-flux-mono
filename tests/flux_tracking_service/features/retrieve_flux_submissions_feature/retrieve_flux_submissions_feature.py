from tests import scenario
from tests.flux_tracking_service.features.retrieve_flux_submissions_feature.retrieve_flux_submissions_feature_steps import \
    lambda_is_invoked, result_is_empty, a_tracked_site_is_added
from tests.flux_tracking_service.infrastructure.common_steps.icos_steps import \
    icos_api_is_configured_to_return_no_submissions


@scenario
def test_when_no_tracked_sites_are_present_in_db(retrieve_flux_submissions_feature):
    ctx = retrieve_flux_submissions_feature
    ctx.runner \
        .when(lambda_is_invoked(ctx)) \
        .then(result_is_empty(ctx)) \
        .run()

@scenario
def test_when_no_submissions_are_available_for_site(retrieve_flux_submissions_feature):
    ctx = retrieve_flux_submissions_feature
    ctx.runner \
        .given(a_tracked_site_is_added(ctx)) \
        .and_also(icos_api_is_configured_to_return_no_submissions(ctx)) \
        .when(lambda_is_invoked(ctx)) \
        .then(result_is_empty(ctx)) \
        .run()