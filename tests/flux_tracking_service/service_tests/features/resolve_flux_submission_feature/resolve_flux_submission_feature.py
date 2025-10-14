from src.flux_tracking_service.flux_submission_resolver.infrastructure.dynamo import SiteNotFoundException
from tests.flux_tracking_service.service_tests.features.resolve_flux_submission_feature.resolve_flux_submission_feature_steps import \
    result_should_be_empty, lambda_is_invoked_with_submission_id_SUBMISSION_ID_and_site_SITE, \
    lambda_should_throw_with_submission_id_SUBMISSION_ID_and_site_SITE, \
    a_tracked_site_is_added_with_last_fetched_LAST_FETCHED
from tests.flux_tracking_service.service_tests.infrastructure.common_steps.icos_steps import \
    icos_api_is_configured_with_submission_OBJECT_ID_to_submission_not_found, \
    icos_api_is_configured_with_submission_OBJECT_ID_to_submission_id_malformed, \
    icos_api_is_configured_with_submission_OBJECT_ID_to_return_files_FILE_URLS_for_submission
from tests.flux_tracking_service.service_tests.infrastructure.common_steps.log_steps import \
    there_should_be_a_log_with_severity_LEVEL_and_message_MESSAGE


def test_when_submission_is_not_found(resolve_flux_submission_feature):
    ctx = resolve_flux_submission_feature
    ctx.runner \
        .given(icos_api_is_configured_with_submission_OBJECT_ID_to_submission_not_found(
            ctx.submission_id,
            ctx.requests_mock
        )) \
        .and_also(a_tracked_site_is_added_with_last_fetched_LAST_FETCHED(ctx)) \
        .when(lambda_is_invoked_with_submission_id_SUBMISSION_ID_and_site_SITE(
            ctx.site,
            ctx.submission_id,
            ctx.submission_timestamp,
            ctx
        )) \
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
        .and_also(a_tracked_site_is_added_with_last_fetched_LAST_FETCHED(ctx)) \
        .when(lambda_is_invoked_with_submission_id_SUBMISSION_ID_and_site_SITE(
            ctx.site,
            ctx.submission_id,
            ctx.submission_timestamp,
            ctx
        )) \
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
        .then(lambda_should_throw_with_submission_id_SUBMISSION_ID_and_site_SITE(
            ctx.site,
            ctx.submission_id,
            ctx.submission_timestamp,
            SiteNotFoundException,
            ctx
        )) \
        .and_also(there_should_be_a_log_with_severity_LEVEL_and_message_MESSAGE(
            f"site {ctx.site} not found",
            "ERROR",
            ctx.container
        )) \
        .run_all_steps()