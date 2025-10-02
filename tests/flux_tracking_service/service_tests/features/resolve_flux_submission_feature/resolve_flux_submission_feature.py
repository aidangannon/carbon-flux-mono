from tests.flux_tracking_service.service_tests.features.resolve_flux_submission_feature.resolve_flux_submission_feature_steps import \
    result_should_be_empty, lambda_is_invoked_with_submission_id_SUBMISSION_ID_and_site_SITE
from tests.flux_tracking_service.service_tests.infrastructure.common_steps.icos_steps import \
    icos_api_is_configured_with_submission_OBJECT_ID_to_submission_not_found, \
    icos_api_is_configured_with_submission_OBJECT_ID_to_submission_id_malformed
from tests.flux_tracking_service.service_tests.infrastructure.common_steps.log_steps import \
    there_should_be_a_log_with_severity_LEVEL_and_message_MESSAGE


def test_when_submission_is_not_found(resolve_flux_submission_feature):
    ctx = resolve_flux_submission_feature
    ctx.runner \
        .given(icos_api_is_configured_with_submission_OBJECT_ID_to_submission_not_found(
            ctx.submission_id,
            ctx.requests_mock)
        ) \
        .when(lambda_is_invoked_with_submission_id_SUBMISSION_ID_and_site_SITE(ctx.submission_id, ctx.site, ctx)) \
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
            ctx.requests_mock)
        ) \
        .when(lambda_is_invoked_with_submission_id_SUBMISSION_ID_and_site_SITE(ctx.submission_id, ctx.site, ctx)) \
        .then(result_should_be_empty(ctx)) \
        .and_also(there_should_be_a_log_with_severity_LEVEL_and_message_MESSAGE(
            f"invalid submission id: {ctx.submission_id}",
            "ERROR",
            ctx.container
        )) \
        .run_all_steps()