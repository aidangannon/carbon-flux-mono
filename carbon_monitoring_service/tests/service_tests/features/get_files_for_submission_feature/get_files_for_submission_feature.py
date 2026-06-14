from carbon_monitoring_service.src.application.exceptions import SiteNotFoundException
from carbon_monitoring_service.src.infrastructure import icos
from carbon_monitoring_service.tests.service_tests.features.get_files_for_submission_feature.steps import (
    GetFilesForSubmissionContext,
    lambda_is_invoked,
    lambda_should_throw,
    monitored_site_is_created,
    result_should_equal_file_url_and_site,
    site_last_fetched_should_be_updated,
)
from carbon_monitoring_service.tests.service_tests.infrastructure.common_steps.icos_steps import (
    icos_api_submission_OBJECT_ID_not_found,
    icos_api_submission_OBJECT_ID_id_malformed,
    icos_api_submission_OBJECT_ID_returns_files_FILE_URLS,
)
from carbon_monitoring_service.tests.service_tests.infrastructure.common_steps.log_steps import (
    should_have_log_LEVEL_MESSAGE,
)


def test_when_submission_is_not_found(
    get_files_for_submission_feature: GetFilesForSubmissionContext,
):
    ctx = get_files_for_submission_feature
    ctx.runner \
        .given(icos_api_submission_OBJECT_ID_not_found(ctx.submission_id, ctx.requests_mock)) \
        .and_also(monitored_site_is_created(ctx)) \
        .then(lambda_should_throw(icos.SubmissionNotFoundException, ctx)) \
        .and_also(should_have_log_LEVEL_MESSAGE(f"no submission contents found for {ctx.submission_id}", "ERROR", ctx.log_capture)) \
        .run_all_steps()


def test_when_submission_is_not_valid_sha256(
    get_files_for_submission_feature: GetFilesForSubmissionContext,
):
    ctx = get_files_for_submission_feature
    ctx.runner \
        .given(icos_api_submission_OBJECT_ID_id_malformed(ctx.submission_id, ctx.requests_mock)) \
        .and_also(monitored_site_is_created(ctx)) \
        .then(lambda_should_throw(icos.SubmissionMalformedException, ctx)) \
        .and_also(should_have_log_LEVEL_MESSAGE(f"invalid submission id: {ctx.submission_id}", "ERROR", ctx.log_capture)) \
        .run_all_steps()


def test_when_site_is_not_found(
    get_files_for_submission_feature: GetFilesForSubmissionContext,
):
    ctx = get_files_for_submission_feature
    ctx.runner \
        .given(icos_api_submission_OBJECT_ID_returns_files_FILE_URLS(ctx.file_urls, ctx.submission_id, ctx.requests_mock)) \
        .then(lambda_should_throw(SiteNotFoundException, ctx)) \
        .and_also(should_have_log_LEVEL_MESSAGE(f"handler failed: site {ctx.site} not found", "ERROR", ctx.log_capture)) \
        .run_all_steps()


def test_when_files_are_fetched_for_site(
    get_files_for_submission_feature: GetFilesForSubmissionContext,
):
    ctx = get_files_for_submission_feature
    ctx.runner \
        .given(icos_api_submission_OBJECT_ID_returns_files_FILE_URLS(ctx.file_urls, ctx.submission_id, ctx.requests_mock)) \
        .and_also(monitored_site_is_created(ctx)) \
        .when(lambda_is_invoked(ctx)) \
        .then(result_should_equal_file_url_and_site(ctx)) \
        .and_also(site_last_fetched_should_be_updated(ctx)) \
        .and_also(should_have_log_LEVEL_MESSAGE("handler started", "INFO", ctx.log_capture)) \
        .and_also(should_have_log_LEVEL_MESSAGE("handler completed", "INFO", ctx.log_capture)) \
        .run_all_steps()
