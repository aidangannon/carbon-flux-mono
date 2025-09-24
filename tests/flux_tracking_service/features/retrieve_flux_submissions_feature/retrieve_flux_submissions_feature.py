from datetime import datetime, timezone, timedelta

from tests import scenario
from tests.flux_tracking_service.features.retrieve_flux_submissions_feature.retrieve_flux_submissions_feature_steps import \
    lambda_is_invoked, result_is_empty, a_tracked_site_is_added_with_last_fetched_LAST_FETCHED
from tests.flux_tracking_service.infrastructure.common_steps.icos_steps import \
    icos_api_is_configured_with_station_STATION_ID_to_return_empty, \
    icos_api_is_configured_with_station_STATION_ID_to_return_submission_OBJECT_ID
from tests.flux_tracking_service.infrastructure.common_steps.log_steps import \
    there_should_be_a_log_with_severity_LEVEL_and_message_MESSAGE


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
        .and_also(icos_api_is_configured_with_station_STATION_ID_to_return_empty(ctx.station, ctx.requests_mock)) \
        .when(lambda_is_invoked(ctx)) \
        .then(result_is_empty(ctx)) \
        .and_also(there_should_be_a_log_with_severity_LEVEL_and_message_MESSAGE(f"no submissions found for {ctx.station}", "ERROR", ctx.container)) \
        .run_all_steps()

@scenario
def test_when_a_submission_is_has_already_been_processed_for_the_site(retrieve_flux_submissions_feature):
    submission_time = datetime.now(tz=timezone.utc)

    ctx = retrieve_flux_submissions_feature
    ctx.runner \
        .given(a_tracked_site_is_added_with_last_fetched_LAST_FETCHED(ctx, last_fetched=submission_time)) \
        .and_also(icos_api_is_configured_with_station_STATION_ID_to_return_submission_OBJECT_ID(ctx.station, ctx.submission, submission_time, ctx.requests_mock)) \
        .when(lambda_is_invoked(ctx)) \
        .then(result_is_empty(ctx)) \
        .and_also(there_should_be_a_log_with_severity_LEVEL_and_message_MESSAGE(f"no new submissions for {ctx.station}", "WARNING", ctx.container)) \
        .run_all_steps()

@scenario
def test_when_a_submission_is_deleted_for_site(retrieve_flux_submissions_feature):
    submission_time = datetime.now(tz=timezone.utc) - timedelta(days=5)
    last_fetched_for_site = datetime.now(tz=timezone.utc)


    ctx = retrieve_flux_submissions_feature
    ctx.runner \
        .given(a_tracked_site_is_added_with_last_fetched_LAST_FETCHED(ctx, last_fetched=last_fetched_for_site)) \
        .and_also(icos_api_is_configured_with_station_STATION_ID_to_return_submission_OBJECT_ID(ctx.station, ctx.submission, submission_time, ctx.requests_mock)) \
        .when(lambda_is_invoked(ctx)) \
        .then(result_is_empty(ctx)) \
        .and_also(there_should_be_a_log_with_severity_LEVEL_and_message_MESSAGE(f"no new submissions for {ctx.station}", "WARNING", ctx.container)) \
        .run_all_steps()