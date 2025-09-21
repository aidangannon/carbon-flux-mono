from tests import step
from tests.flux_tracking_service.infrastructure.api_mocks import icos


@step
def icos_api_is_configured_to_return_latest_submission(
    context,
    station_url: str,
    datatype_url: str,
    submission_object_id: str
):
    icos.configure_get_submissions(
        station=station_url,
        datatype=datatype_url,
        order_desc_field="timeEnd",
        submission_object=submission_object_id,
        limit=1,
        request_mock=context.request_mock
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
        request_mock=context.request_mock
    )