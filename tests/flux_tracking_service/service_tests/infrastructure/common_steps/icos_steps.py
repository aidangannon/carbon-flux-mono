from datetime import datetime

from responses import RequestsMock

from tests import step
from tests.flux_tracking_service.service_tests.infrastructure.api_mocks import icos
from tests.flux_tracking_service.service_tests.infrastructure.api_mocks.icos import Submission

TIME_END_FIELD = "timeEnd"
EDDY_FLUX_RAW_DATA_TYPE = "etcEddyFluxRawSeriesCsv"


@step
def icos_api_is_configured_to_return_submissions_SUBMISSIONS(submissions: dict[str, Submission], requests_mock: RequestsMock):
    icos.configure_get_etc_submissions_with_latest(
        datatype=EDDY_FLUX_RAW_DATA_TYPE,
        submissions=submissions,
        request_mock=requests_mock
    )

@step
def icos_api_is_configured_to_return_empty(requests_mock: RequestsMock):
    icos.configure_get_etc_submissions_with_bindings(
        datatype=EDDY_FLUX_RAW_DATA_TYPE,
        bindings=[],
        request_mock=requests_mock
    )

@step
def icos_api_is_configured_with_submission_OBJECT_ID_to_submission_not_found(
    object_id: str,
    requests_mock: RequestsMock
):
    icos.configure_get_content_with_string(
        body=f"""No metadata found for data object with SHA-256 hash of {object_id}
se.lu.nateko.cp.data.api.MetadataObjectNotFound: No metadata found for data object with SHA-256 hash of {object_id}
""",
        submission_object=object_id,
        request_mock=requests_mock,
        status=500
    )

@step
def icos_api_is_configured_with_submission_OBJECT_ID_to_submission_id_malformed(
    object_id: str,
    requests_mock: RequestsMock
):
    icos.configure_get_content_with_string(
        body="Expected base64Url- or hex-encoded SHA-256 hash",
        submission_object=object_id,
        request_mock=requests_mock,
        status=400
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

@step
def icos_api_is_configured_to_return_invalid_submission_url_with_submission_time_SUBMISSION_TIME_and_tracked_site_TRACKED_SITE(
    submission_time: datetime,
    site: str,
    requests_mock: RequestsMock
):
    icos.configure_get_etc_submissions_with_invalid_submission_id(
        datatype=EDDY_FLUX_RAW_DATA_TYPE,
        submission_time=submission_time,
        site=site,
        request_mock=requests_mock
    )