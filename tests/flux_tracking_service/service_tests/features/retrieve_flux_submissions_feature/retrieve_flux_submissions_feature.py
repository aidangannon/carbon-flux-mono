from datetime import datetime, timezone, timedelta

from src.flux_tracking_service.flux_submission_detector.infrastructure.icos import SubmissionObjectIdMalformed
from tests.flux_tracking_service.service_tests.features.retrieve_flux_submissions_feature.retrieve_flux_submissions_feature_steps import \
    lambda_is_invoked, result_is_empty, a_tracked_site_is_added_with_last_fetched_LAST_FETCHED, \
    a_submission_exists_for_tracked_site_TRACKED_SITE, \
    lambda_should_throw_error, result_has_submissions_SUBMISSIONS_for_tracked_sites
from tests.flux_tracking_service.service_tests.infrastructure.common_steps.icos_steps import \
    icos_api_is_configured_to_return_empty, icos_api_is_configured_to_return_invalid_submission_url_with_submission_time_SUBMISSION_TIME_and_tracked_site_TRACKED_SITE, \
    icos_api_is_configured_to_return_submissions_SUBMISSIONS
from tests.flux_tracking_service.service_tests.infrastructure.common_steps.log_steps import \
    there_should_be_a_log_with_severity_LEVEL_and_message_MESSAGE, \
    there_should_be_a_log_with_severity_LEVEL_and_message_MESSAGE_and_extras_EXTRAS


def test_when_no_tracked_sites_are_present_in_db(retrieve_flux_submissions_feature):
    ctx = retrieve_flux_submissions_feature
    ctx.runner \
        .when(lambda_is_invoked(ctx)) \
        .then(result_is_empty(ctx)) \
        .run_all_steps()

def test_when_no_submissions_are_available_for_site(retrieve_flux_submissions_feature):
    ctx = retrieve_flux_submissions_feature
    ctx.runner \
        .given(a_tracked_site_is_added_with_last_fetched_LAST_FETCHED(ctx)) \
        .and_also(icos_api_is_configured_to_return_empty(ctx.requests_mock)) \
        .when(lambda_is_invoked(ctx)) \
        .then(result_is_empty(ctx)) \
        .and_also(there_should_be_a_log_with_severity_LEVEL_and_message_MESSAGE(
            "no submissions found",
            "ERROR",
            ctx.container)) \
        .run_all_steps()

def test_when_submission_url_is_malformed(retrieve_flux_submissions_feature):
    submission_time = datetime.now(tz=timezone.utc)

    ctx = retrieve_flux_submissions_feature
    ctx.runner \
        .given(a_tracked_site_is_added_with_last_fetched_LAST_FETCHED(ctx)) \
        .and_also(icos_api_is_configured_to_return_invalid_submission_url_with_submission_time_SUBMISSION_TIME_and_tracked_site_TRACKED_SITE(
            submission_time,
            ctx.tracked_sites[0].name,
            ctx.requests_mock)
        ) \
        .then(lambda_should_throw_error(ctx, SubmissionObjectIdMalformed)) \
        .and_also(there_should_be_a_log_with_severity_LEVEL_and_message_MESSAGE_and_extras_EXTRAS(
            "handler failed: submission object id malformed: invalid_unparsable",
            "ERROR",
            ctx.scoped_log_vars,
            ctx.container)) \
        .run_all_steps()

def test_when_a_submission_is_has_already_been_processed_for_the_site(retrieve_flux_submissions_feature):
    submission_time = datetime.now(tz=timezone.utc)

    ctx = retrieve_flux_submissions_feature
    ctx.runner \
        .given(a_tracked_site_is_added_with_last_fetched_LAST_FETCHED(ctx, submission_time)) \
        .and_also(a_submission_exists_for_tracked_site_TRACKED_SITE(ctx.tracked_sites[0].name, submission_time, ctx)) \
        .and_also(icos_api_is_configured_to_return_submissions_SUBMISSIONS(ctx.submissions, ctx.requests_mock)) \
        .when(lambda_is_invoked(ctx)) \
        .then(result_is_empty(ctx)) \
        .run_all_steps()

def test_when_a_submission_is_deleted_for_site(retrieve_flux_submissions_feature):
    last_fetched_for_site = datetime.now(tz=timezone.utc)
    submission_time = last_fetched_for_site - timedelta(days=5)

    ctx = retrieve_flux_submissions_feature
    ctx.runner \
        .given(a_tracked_site_is_added_with_last_fetched_LAST_FETCHED(ctx, last_fetched_for_site)) \
        .and_also(a_submission_exists_for_tracked_site_TRACKED_SITE(ctx.tracked_sites[0].name, submission_time, ctx)) \
        .and_also(icos_api_is_configured_to_return_submissions_SUBMISSIONS(ctx.submissions, ctx.requests_mock)) \
        .when(lambda_is_invoked(ctx)) \
        .then(result_is_empty(ctx)) \
        .run_all_steps()

def test_when_a_new_submission_is_added_for_site(retrieve_flux_submissions_feature):
    submission_time = datetime.now(tz=timezone.utc)
    last_fetched_for_site = submission_time - timedelta(days=1)

    ctx = retrieve_flux_submissions_feature
    ctx.runner \
        .given(a_tracked_site_is_added_with_last_fetched_LAST_FETCHED(ctx, last_fetched=last_fetched_for_site)) \
        .and_also(a_submission_exists_for_tracked_site_TRACKED_SITE(ctx.tracked_sites[0].name, submission_time, ctx)) \
        .and_also(icos_api_is_configured_to_return_submissions_SUBMISSIONS(ctx.submissions, ctx.requests_mock)) \
        .when(lambda_is_invoked(ctx)) \
        .then(result_has_submissions_SUBMISSIONS_for_tracked_sites(ctx.submissions, ctx)) \
        .and_also(there_should_be_a_log_with_severity_LEVEL_and_message_MESSAGE_and_extras_EXTRAS(
            f"handler started",
            "INFO",
            ctx.scoped_log_vars,
            ctx.container,
        )) \
        .and_also(there_should_be_a_log_with_severity_LEVEL_and_message_MESSAGE_and_extras_EXTRAS(
            f"handler completed",
            "INFO",
            ctx.scoped_log_vars,
            ctx.container
        )) \
        .run_all_steps()

def test_when_first_submission_is_added_for_site(retrieve_flux_submissions_feature):
    submission_time = datetime.now(tz=timezone.utc)

    ctx = retrieve_flux_submissions_feature
    ctx.runner \
        .given(a_tracked_site_is_added_with_last_fetched_LAST_FETCHED(ctx)) \
        .and_also(a_submission_exists_for_tracked_site_TRACKED_SITE(ctx.tracked_sites[0].name, submission_time, ctx)) \
        .and_also(icos_api_is_configured_to_return_submissions_SUBMISSIONS(ctx.submissions, ctx.requests_mock)) \
        .when(lambda_is_invoked(ctx)) \
        .then(result_has_submissions_SUBMISSIONS_for_tracked_sites(ctx.submissions, ctx)) \
        .run_all_steps()

def test_when_multiple_submissions_are_added_for_different_sites(retrieve_flux_submissions_feature):
    submission_time = datetime.now(tz=timezone.utc)
    last_fetched = datetime.now(tz=timezone.utc) - timedelta(days=5)

    ctx = retrieve_flux_submissions_feature
    ctx.runner \
        .given(a_tracked_site_is_added_with_last_fetched_LAST_FETCHED(ctx, last_fetched)) \
        .and_also(a_tracked_site_is_added_with_last_fetched_LAST_FETCHED(ctx)) \
        .and_also(a_tracked_site_is_added_with_last_fetched_LAST_FETCHED(ctx)) \
        .and_also(a_submission_exists_for_tracked_site_TRACKED_SITE(ctx.tracked_sites[0].name, submission_time, ctx)) \
        .and_also(a_submission_exists_for_tracked_site_TRACKED_SITE(ctx.tracked_sites[1].name, submission_time, ctx)) \
        .and_also(a_submission_exists_for_tracked_site_TRACKED_SITE(ctx.tracked_sites[2].name, submission_time, ctx)) \
        .and_also(icos_api_is_configured_to_return_submissions_SUBMISSIONS(ctx.submissions, ctx.requests_mock)) \
        .when(lambda_is_invoked(ctx)) \
        .then(result_has_submissions_SUBMISSIONS_for_tracked_sites(ctx.submissions, ctx)) \
        .run_all_steps()