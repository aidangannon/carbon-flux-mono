from datetime import datetime, timezone, timedelta

from carbon_monitoring_service.src.infrastructure.icos import (
    SubmissionObjectIdMalformed,
)
from carbon_monitoring_service.tests.service_tests.features.get_latest_submissions_feature.steps import (
    GetLatestSubmissionsContext,
    lambda_is_invoked,
    result_should_be_empty,
    site_created_with_last_fetched_FETCHED,
    submission_created_for_site_SITE,
    lambda_should_throw_error,
    result_should_have_submissions_SUBS,
)
from carbon_monitoring_service.tests.service_tests.infrastructure.common_steps.icos_steps import (
    icos_api_returns_empty,
    icos_api_invalid_submission_url_SUBMISSION_TIME_MONITORED_SITE,
    icos_api_returns_submissions_SUBMISSIONS,
)
from carbon_monitoring_service.tests.service_tests.infrastructure.common_steps.log_steps import (
    should_have_log_LEVEL_MESSAGE,
    should_have_log_LEVEL_MESSAGE_EXTRAS,
)


def test_when_no_submissions_are_available_for_site(
    get_latest_submissions_feature: GetLatestSubmissionsContext,
):
    ctx = get_latest_submissions_feature
    ctx.runner \
        .given(site_created_with_last_fetched_FETCHED(ctx)) \
        .and_also(icos_api_returns_empty(ctx.requests_mock)) \
        .when(lambda_is_invoked(ctx)) \
        .then(result_should_be_empty(ctx)) \
        .and_also(should_have_log_LEVEL_MESSAGE("no submissions found", "ERROR", ctx.log_capture)) \
        .run_all_steps()


def test_when_submission_url_is_malformed(
    get_latest_submissions_feature: GetLatestSubmissionsContext,
):
    submission_time = datetime.now(tz=timezone.utc)

    ctx = get_latest_submissions_feature
    ctx.runner \
        .given(site_created_with_last_fetched_FETCHED(ctx)) \
        .and_also(icos_api_invalid_submission_url_SUBMISSION_TIME_MONITORED_SITE(submission_time, ctx.monitored_sites[0].name, ctx.requests_mock)) \
        .then(lambda_should_throw_error(ctx, SubmissionObjectIdMalformed)) \
        .and_also(should_have_log_LEVEL_MESSAGE_EXTRAS("handler failed: submission object id malformed: invalid_unparsable", "ERROR", ctx.scoped_log_vars, ctx.log_capture)) \
        .run_all_steps()


def test_when_a_submission_is_has_already_been_processed_for_the_site(
    get_latest_submissions_feature: GetLatestSubmissionsContext,
):
    submission_time = datetime.now(tz=timezone.utc)

    ctx = get_latest_submissions_feature
    ctx.runner \
        .given(site_created_with_last_fetched_FETCHED(ctx, submission_time)) \
        .and_also(submission_created_for_site_SITE(ctx.monitored_sites[0].name, submission_time, ctx)) \
        .and_also(icos_api_returns_submissions_SUBMISSIONS(ctx.submissions, ctx.requests_mock)) \
        .when(lambda_is_invoked(ctx)) \
        .then(result_should_be_empty(ctx)) \
        .run_all_steps()


def test_when_a_submission_is_deleted_for_site(
    get_latest_submissions_feature: GetLatestSubmissionsContext,
):
    last_fetched_for_site = datetime.now(tz=timezone.utc)
    submission_time = last_fetched_for_site - timedelta(days=5)

    ctx = get_latest_submissions_feature
    ctx.runner \
        .given(site_created_with_last_fetched_FETCHED(ctx, last_fetched_for_site)) \
        .and_also(submission_created_for_site_SITE(ctx.monitored_sites[0].name, submission_time, ctx)) \
        .and_also(icos_api_returns_submissions_SUBMISSIONS(ctx.submissions, ctx.requests_mock)) \
        .when(lambda_is_invoked(ctx)) \
        .then(result_should_be_empty(ctx)) \
        .run_all_steps()


def test_when_a_new_submission_is_added_for_site(
    get_latest_submissions_feature: GetLatestSubmissionsContext,
):
    submission_time = datetime.now(tz=timezone.utc)
    last_fetched_for_site = submission_time - timedelta(days=1)

    ctx = get_latest_submissions_feature
    ctx.runner \
        .given(site_created_with_last_fetched_FETCHED(ctx, fetched=last_fetched_for_site)) \
        .and_also(submission_created_for_site_SITE(ctx.monitored_sites[0].name, submission_time, ctx)) \
        .and_also(icos_api_returns_submissions_SUBMISSIONS(ctx.submissions, ctx.requests_mock)) \
        .when(lambda_is_invoked(ctx)) \
        .then(result_should_have_submissions_SUBS(ctx.submissions, ctx)) \
        .and_also(should_have_log_LEVEL_MESSAGE_EXTRAS("handler started", "INFO", ctx.scoped_log_vars, ctx.log_capture)) \
        .and_also(should_have_log_LEVEL_MESSAGE_EXTRAS("handler completed", "INFO", ctx.scoped_log_vars, ctx.log_capture)) \
        .run_all_steps()


def test_when_first_submission_is_added_for_site(
    get_latest_submissions_feature: GetLatestSubmissionsContext,
):
    submission_time = datetime.now(tz=timezone.utc)

    ctx = get_latest_submissions_feature
    ctx.runner \
        .given(site_created_with_last_fetched_FETCHED(ctx)) \
        .and_also(submission_created_for_site_SITE(ctx.monitored_sites[0].name, submission_time, ctx)) \
        .and_also(icos_api_returns_submissions_SUBMISSIONS(ctx.submissions, ctx.requests_mock)) \
        .when(lambda_is_invoked(ctx)) \
        .then(result_should_have_submissions_SUBS(ctx.submissions, ctx)) \
        .run_all_steps()


def test_when_multiple_submissions_are_added_for_different_sites(
    get_latest_submissions_feature: GetLatestSubmissionsContext,
):
    submission_time = datetime.now(tz=timezone.utc)
    last_fetched = datetime.now(tz=timezone.utc) - timedelta(days=5)

    ctx = get_latest_submissions_feature
    ctx.runner \
        .given(site_created_with_last_fetched_FETCHED(ctx, last_fetched)) \
        .and_also(site_created_with_last_fetched_FETCHED(ctx)) \
        .and_also(site_created_with_last_fetched_FETCHED(ctx)) \
        .and_also(submission_created_for_site_SITE(ctx.monitored_sites[0].name, submission_time, ctx)) \
        .and_also(submission_created_for_site_SITE(ctx.monitored_sites[1].name, submission_time, ctx)) \
        .and_also(submission_created_for_site_SITE(ctx.monitored_sites[2].name, submission_time, ctx)) \
        .and_also(icos_api_returns_submissions_SUBMISSIONS(ctx.submissions, ctx.requests_mock)) \
        .when(lambda_is_invoked(ctx)) \
        .then(result_should_have_submissions_SUBS(ctx.submissions, ctx)) \
        .run_all_steps()
