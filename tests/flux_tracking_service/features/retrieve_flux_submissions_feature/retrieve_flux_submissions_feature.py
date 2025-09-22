from tests import scenario
from tests.flux_tracking_service.features.retrieve_flux_submissions_feature.retrieve_flux_submissions_feature_steps import \
    lambda_is_invoked, result_is_empty, a_tracked_site_is_added_with_last_fetched_LAST_FETCHED
from tests.flux_tracking_service.infrastructure.common_steps.icos_steps import \
    icos_api_is_configured_with_station_STATION_ID_to_return_empty


@scenario
def test_when_no_tracked_sites_are_present_in_db(retrieve_flux_submissions_feature):
    ctx = retrieve_flux_submissions_feature
    ctx.runner \
        .when(lambda_is_invoked(ctx)) \
        .then(result_is_empty(ctx)) \
        .run_all_steps()

@scenario
def test_when_no_submissions_are_available_for_site(retrieve_flux_submissions_feature):
    ctx = retrieve_flux_submissions_feature
    ctx.runner \
        .given(a_tracked_site_is_added_with_last_fetched_LAST_FETCHED(ctx)) \
        .and_also(icos_api_is_configured_with_station_STATION_ID_to_return_empty(ctx.station_id, ctx.requests_mock)) \
        .when(lambda_is_invoked(ctx)) \
        .then(result_is_empty(ctx)) \
        .run_all_steps()