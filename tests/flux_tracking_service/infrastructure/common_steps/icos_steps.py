from tests import step
from tests.flux_tracking_service.infrastructure.api_mocks import icos

TIME_END_FIELD = "timeEnd"
EDDY_FLUX_RAW_DATA_TYPE = "etcEddyFluxRawSeriesCsv"


@step
def icos_api_is_configured_to_return_latest_submission(
    context,
    station_id: str,
    submission_object_id: str
):
    icos.configure_get_etc_submissions_with_latest(
        station=station_id,
        datatype=EDDY_FLUX_RAW_DATA_TYPE,
        order_desc_field=TIME_END_FIELD,
        submission_object=submission_object_id,
        limit=1,
        request_mock=context.requests_mock
    )

@step
def icos_api_is_configured_to_return_no_submissions(
    context
):
    icos.configure_get_etc_submissions_with_bindings(
        station=context.station_id,
        datatype=EDDY_FLUX_RAW_DATA_TYPE,
        order_desc_field=TIME_END_FIELD,
        bindings=[],
        limit=1,
        request_mock=context.requests_mock
    )

@step
def icos_api_is_configured_to_return_files_for_submission(
    context,
    file_urls: list[str],
    submission_object_id: str
):
    icos.configure_get_content(
        file_urls=file_urls,
        submission_object=submission_object_id,
        request_mock=context.requests_mock
    )