from src.carbon_tracking_service.flux_submission_resolver.infrastructure.dynamo import SiteNotFoundException
from tests.carbon_tracking_service.service_tests.features.get_files_for_submission_feature.get_files_for_submission_feature_steps import \
    result_should_be_empty, lambda_is_invoked, \
    lambda_should_throw, \
    a_tracked_site_is_added, result_should_contain_map_file_url_and_site, the_tracked_sites_last_fetched_is_updated
from tests.carbon_tracking_service.service_tests.infrastructure.common_steps.icos_steps import \
    icos_api_is_configured_with_submission_OBJECT_ID_to_submission_not_found, \
    icos_api_is_configured_with_submission_OBJECT_ID_to_submission_id_malformed, \
    icos_api_is_configured_with_submission_OBJECT_ID_to_return_files_FILE_URLS_for_submission
from tests.carbon_tracking_service.service_tests.infrastructure.common_steps.log_steps import \
    there_should_be_a_log_with_severity_LEVEL_and_message_MESSAGE


def test_when_submission_is_not_found(resolve_flux_submission_feature):
    ctx = resolve_flux_submission_feature
    ctx.runner \
        .given(icos_api_is_configured_with_submission_OBJECT_ID_to_submission_not_found(
            ctx.submission_id,
            ctx.requests_mock
        )) \
        .and_also(a_tracked_site_is_added(ctx)) \
        .when(lambda_is_invoked(ctx)) \
        .then(result_should_be_empty(ctx)) \
        .and_also(there_should_be_a_log_with_severity_LEVEL_and_message_MESSAGE(
            f"no submission contents found for {ctx.submission_id}",
            "ERROR",
            ctx.container
        )) \
        .run_all_steps()

def test_when_submission_is_not_valid_sha256(resolve_flux_submission_feature):
    ctx = resolve_flux_submission_feature
    ctx.runner \
        .given(icos_api_is_configured_with_submission_OBJECT_ID_to_submission_id_malformed(
            ctx.submission_id,
            ctx.requests_mock
        )) \
        .and_also(a_tracked_site_is_added(ctx)) \
        .when(lambda_is_invoked(ctx)) \
        .then(result_should_be_empty(ctx)) \
        .and_also(there_should_be_a_log_with_severity_LEVEL_and_message_MESSAGE(
            f"invalid submission id: {ctx.submission_id}",
            "ERROR",
            ctx.container
        )) \
        .run_all_steps()

def test_when_site_is_not_found(resolve_flux_submission_feature):
    ctx = resolve_flux_submission_feature
    ctx.runner \
        .given(icos_api_is_configured_with_submission_OBJECT_ID_to_return_files_FILE_URLS_for_submission(
            ctx.file_urls,
            ctx.submission_id,
            ctx.requests_mock
        )) \
        .then(lambda_should_throw(SiteNotFoundException, ctx)) \
        .and_also(there_should_be_a_log_with_severity_LEVEL_and_message_MESSAGE(
            f"site {ctx.site} not found",
            "ERROR",
            ctx.container
        )) \
        .run_all_steps()
    
    
def test_when_files_are_fetched_for_site(resolve_flux_submission_feature):
    ctx = resolve_flux_submission_feature
    ctx.runner \
        .given(icos_api_is_configured_with_submission_OBJECT_ID_to_return_files_FILE_URLS_for_submission(
            ctx.file_urls,
            ctx.submission_id,
            ctx.requests_mock
        )) \
        .and_also(a_tracked_site_is_added(ctx)) \
        .when(lambda_is_invoked(ctx)) \
        .then(result_should_contain_map_file_url_and_site(ctx)) \
        .and_also(the_tracked_sites_last_fetched_is_updated(ctx)) \
        .and_also(there_should_be_a_log_with_severity_LEVEL_and_message_MESSAGE(
            f"site {ctx.site} not found",
            "ERROR",
            ctx.container
        )) \
        .run_all_steps()