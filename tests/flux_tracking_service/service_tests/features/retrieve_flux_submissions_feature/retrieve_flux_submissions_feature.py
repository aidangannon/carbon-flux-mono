from datetime import datetime, timezone, timedelta

from tests.flux_tracking_service.service_tests.features.retrieve_flux_submissions_feature.retrieve_flux_submissions_feature_steps import \
    lambda_is_invoked, result_is_empty, a_tracked_site_is_added_with_last_fetched_LAST_FETCHED, \
    a_submission_exists_for_tracked_site_TRACKED_SITE, result_has_submissions_SUBMISSIONS_for_tracked_site_TRACKED_SITE
from tests.flux_tracking_service.service_tests.infrastructure.common_steps.icos_steps import \
    icos_api_is_configured_with_station_STATION_ID_to_return_empty, \
    icos_api_is_configured_with_station_STATION_ID_to_return_submission_OBJECT_ID, \
    icos_api_is_configured_with_submission_OBJECT_ID_to_return_files_FILE_URLS_for_submission
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
        .and_also(icos_api_is_configured_with_station_STATION_ID_to_return_empty(ctx.tracked_sites[0].name, ctx.requests_mock)) \
        .when(lambda_is_invoked(ctx)) \
        .then(result_is_empty(ctx)) \
        .and_also(there_should_be_a_log_with_severity_LEVEL_and_message_MESSAGE(
            f"no submissions found for {ctx.tracked_sites[0].name}",
            "ERROR",
            ctx.container)) \
        .run_all_steps()

def test_when_a_submission_is_has_already_been_processed_for_the_site(retrieve_flux_submissions_feature):
    submission_time = datetime.now(tz=timezone.utc)

    ctx = retrieve_flux_submissions_feature
    ctx.runner \
        .given(a_tracked_site_is_added_with_last_fetched_LAST_FETCHED(ctx, submission_time)) \
        .and_also(a_submission_exists_for_tracked_site_TRACKED_SITE(ctx.tracked_sites[0].name, ctx)) \
        .and_also(icos_api_is_configured_with_station_STATION_ID_to_return_submission_OBJECT_ID(
            ctx.tracked_sites[0].name,
            ctx.submission_contents[ctx.tracked_sites[0].name].submission_id,
            submission_time,
            ctx.requests_mock
        )) \
        .when(lambda_is_invoked(ctx)) \
        .then(result_is_empty(ctx)) \
        .and_also(there_should_be_a_log_with_severity_LEVEL_and_message_MESSAGE(
            f"no new submissions for {ctx.tracked_sites[0].name}",
            "WARNING",
            ctx.container
        )) \
        .run_all_steps()

def test_when_a_submission_is_deleted_for_site(retrieve_flux_submissions_feature):
    last_fetched_for_site = datetime.now(tz=timezone.utc)
    submission_time = last_fetched_for_site - timedelta(days=5)

    ctx = retrieve_flux_submissions_feature
    ctx.runner \
        .given(a_tracked_site_is_added_with_last_fetched_LAST_FETCHED(ctx, last_fetched_for_site)) \
        .and_also(a_submission_exists_for_tracked_site_TRACKED_SITE(ctx.tracked_sites[0].name, ctx)) \
        .and_also(icos_api_is_configured_with_station_STATION_ID_to_return_submission_OBJECT_ID(
            ctx.tracked_sites[0].name,
            ctx.submission_contents[ctx.tracked_sites[0].name].submission_id,
            submission_time,
            ctx.requests_mock
        )) \
        .when(lambda_is_invoked(ctx)) \
        .then(result_is_empty(ctx)) \
        .and_also(there_should_be_a_log_with_severity_LEVEL_and_message_MESSAGE(
            f"no new submissions for {ctx.tracked_sites[0].name}",
            "WARNING",
            ctx.container
        )) \
        .run_all_steps()

def test_when_a_new_submission_is_added_for_site(retrieve_flux_submissions_feature):
    submission_time = datetime.now(tz=timezone.utc)
    last_fetched_for_site = submission_time - timedelta(days=1)

    ctx = retrieve_flux_submissions_feature
    ctx.runner \
        .given(a_tracked_site_is_added_with_last_fetched_LAST_FETCHED(ctx, last_fetched=last_fetched_for_site)) \
        .and_also(a_submission_exists_for_tracked_site_TRACKED_SITE(ctx.tracked_sites[0].name, ctx)) \
        .and_also(icos_api_is_configured_with_station_STATION_ID_to_return_submission_OBJECT_ID(
            ctx.tracked_sites[0].name,
            ctx.submission_contents[ctx.tracked_sites[0].name].submission_id,
            submission_time,
            ctx.requests_mock
        )) \
        .and_also(icos_api_is_configured_with_submission_OBJECT_ID_to_return_files_FILE_URLS_for_submission(
            ctx.submission_contents[ctx.tracked_sites[0].name].file_urls,
            ctx.submission_contents[ctx.tracked_sites[0].name].submission_id,
            ctx.requests_mock
        )) \
        .when(lambda_is_invoked(ctx)) \
        .then(result_has_submissions_SUBMISSIONS_for_tracked_site_TRACKED_SITE(
            ctx.submission_contents[ctx.tracked_sites[0].name].file_urls,
            ctx.tracked_sites[0].name,
            ctx
        )) \
        .and_also(there_should_be_a_log_with_severity_LEVEL_and_message_MESSAGE_and_extras_EXTRAS(
            f"ingestion started",
            "INFO",
            ctx.scoped_log_vars,
            ctx.container,
        )) \
        .and_also(there_should_be_a_log_with_severity_LEVEL_and_message_MESSAGE_and_extras_EXTRAS(
            f"ingestion completed",
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
        .and_also(a_submission_exists_for_tracked_site_TRACKED_SITE(ctx.tracked_sites[0].name, ctx)) \
        .and_also(icos_api_is_configured_with_station_STATION_ID_to_return_submission_OBJECT_ID(
            ctx.tracked_sites[0].name,
            ctx.submission_contents[ctx.tracked_sites[0].name].submission_id,
            submission_time,
            ctx.requests_mock
        )) \
        .and_also(icos_api_is_configured_with_submission_OBJECT_ID_to_return_files_FILE_URLS_for_submission(
            ctx.submission_contents[ctx.tracked_sites[0].name].file_urls,
            ctx.submission_contents[ctx.tracked_sites[0].name].submission_id,
            ctx.requests_mock
        )) \
        .when(lambda_is_invoked(ctx)) \
        .then(result_has_submissions_SUBMISSIONS_for_tracked_site_TRACKED_SITE(
            ctx.submission_contents[ctx.tracked_sites[0].name].file_urls,
            ctx.tracked_sites[0].name,
            ctx
        )) \
        .run_all_steps()

def test_when_multiple_submissions_are_added_for_different_sites(retrieve_flux_submissions_feature):
    submission_time = datetime.now(tz=timezone.utc)
    last_fetched = datetime.now(tz=timezone.utc) - timedelta(days=5)

    ctx = retrieve_flux_submissions_feature
    ctx.runner \
        .given(a_tracked_site_is_added_with_last_fetched_LAST_FETCHED(ctx, last_fetched)) \
        .and_also(a_tracked_site_is_added_with_last_fetched_LAST_FETCHED(ctx)) \
        .and_also(a_tracked_site_is_added_with_last_fetched_LAST_FETCHED(ctx)) \
        .and_also(a_submission_exists_for_tracked_site_TRACKED_SITE(ctx.tracked_sites[0].name, ctx)) \
        .and_also(a_submission_exists_for_tracked_site_TRACKED_SITE(ctx.tracked_sites[1].name, ctx)) \
        .and_also(a_submission_exists_for_tracked_site_TRACKED_SITE(ctx.tracked_sites[2].name, ctx)) \
        .and_also(icos_api_is_configured_with_station_STATION_ID_to_return_submission_OBJECT_ID(
            ctx.tracked_sites[0].name,
            ctx.submission_contents[ctx.tracked_sites[0].name].submission_id,
            submission_time,
            ctx.requests_mock
        )) \
        .and_also(icos_api_is_configured_with_station_STATION_ID_to_return_submission_OBJECT_ID(
            ctx.tracked_sites[1].name,
            ctx.submission_contents[ctx.tracked_sites[1].name].submission_id,
            submission_time,
            ctx.requests_mock
        )) \
        .and_also(icos_api_is_configured_with_station_STATION_ID_to_return_submission_OBJECT_ID(
            ctx.tracked_sites[2].name,
            ctx.submission_contents[ctx.tracked_sites[2].name].submission_id,
            submission_time,
            ctx.requests_mock
        )) \
        .and_also(icos_api_is_configured_with_submission_OBJECT_ID_to_return_files_FILE_URLS_for_submission(
            ctx.submission_contents[ctx.tracked_sites[0].name].file_urls,
            ctx.submission_contents[ctx.tracked_sites[0].name].submission_id,
            ctx.requests_mock
        )) \
        .and_also(icos_api_is_configured_with_submission_OBJECT_ID_to_return_files_FILE_URLS_for_submission(
            ctx.submission_contents[ctx.tracked_sites[1].name].file_urls,
            ctx.submission_contents[ctx.tracked_sites[1].name].submission_id,
            ctx.requests_mock
        )) \
        .and_also(icos_api_is_configured_with_submission_OBJECT_ID_to_return_files_FILE_URLS_for_submission(
            ctx.submission_contents[ctx.tracked_sites[2].name].file_urls,
            ctx.submission_contents[ctx.tracked_sites[2].name].submission_id,
            ctx.requests_mock
        )) \
        .when(lambda_is_invoked(ctx)) \
        .then(result_has_submissions_SUBMISSIONS_for_tracked_site_TRACKED_SITE(
            ctx.submission_contents[ctx.tracked_sites[0].name].file_urls,
            ctx.tracked_sites[0].name,
            ctx
        )) \
        .then(result_has_submissions_SUBMISSIONS_for_tracked_site_TRACKED_SITE(
            ctx.submission_contents[ctx.tracked_sites[1].name].file_urls,
            ctx.tracked_sites[1].name,
            ctx
        )) \
        .then(result_has_submissions_SUBMISSIONS_for_tracked_site_TRACKED_SITE(
            ctx.submission_contents[ctx.tracked_sites[2].name].file_urls,
            ctx.tracked_sites[2].name,
            ctx
        )) \
        .run_all_steps()