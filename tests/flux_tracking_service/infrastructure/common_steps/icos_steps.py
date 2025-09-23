from datetime import datetime

from responses import RequestsMock

from tests import step
from tests.flux_tracking_service.infrastructure.api_mocks import icos

TIME_END_FIELD = "timeEnd"
EDDY_FLUX_RAW_DATA_TYPE = "etcEddyFluxRawSeriesCsv"


@step
def icos_api_is_configured_with_station_STATION_ID_to_return_submission_OBJECT_ID(
    station_id: str,
    object_id: str,
    submission_time: datetime,
    requests_mock: RequestsMock
):
    icos.configure_get_etc_submissions_with_latest(
        station=station_id,
        datatype=EDDY_FLUX_RAW_DATA_TYPE,
        order_desc_field=TIME_END_FIELD,
        submission_object=object_id,
        submission_time=submission_time,
        limit=1,
        request_mock=requests_mock
    )

@step
def icos_api_is_configured_with_station_STATION_ID_to_return_empty(
    station_id: str,
    requests_mock: RequestsMock
):
    icos.configure_get_etc_submissions_with_bindings(
        station=station_id,
        datatype=EDDY_FLUX_RAW_DATA_TYPE,
        order_desc_field=TIME_END_FIELD,
        bindings=[],
        limit=1,
        request_mock=requests_mock
    )

@step
def icos_api_is_configured_with_submission_OBJECT_ID_to_return_files_FILE_URLS_for_submission(
    file_urls: list[str],
    object_id: str,
    requests_mock: RequestsMock
):
    icos.configure_get_content(
        file_urls=file_urls,
        submission_object=object_id,
        request_mock=requests_mock
    )