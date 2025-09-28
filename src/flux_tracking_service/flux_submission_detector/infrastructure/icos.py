from dataclasses import dataclass

import requests
from icoscp_core.icos import meta

from src.common.logging import Logger
from src.flux_tracking_service.core import TrackedSite, SiteId
from src.flux_tracking_service.flux_submission_detector.config import IcosSettings
from src.flux_tracking_service.flux_submission_detector.core import FileUrl


def parse_submission_id(uri: str, site: SiteId) -> str:
    parts = uri.split('/')

    if len(parts) < 5:
        raise SubmissionObjectIdMalformed(site)

    return parts[4]


def get_file_paths_for_submission(api_url: str, submission_id: str):
    content_response = requests.get(f"{api_url}/zip/{submission_id}/listContents")
    json_files = content_response.json()

    return [file["path"] for file in json_files if "path" in file]


class SubmissionObjectIdMalformed(Exception):

    def __init__(self, site: SiteId):
        super().__init__(f"submission object id malformed for site {site}")

@dataclass(frozen=True, slots=True)
class Submission:
    submission_id: str
    file_urls: list[FileUrl]

@dataclass(frozen=True, slots=True)
class IcosGetFileUrlsForSite:
    settings: IcosSettings
    logger: Logger

    def __call__(self, site: TrackedSite) -> list[FileUrl]:
        response_from_icos = meta.list_data_objects(
            datatype=f'{self.settings.meta_url}/resources/cpmeta/etcEddyFluxRawSeriesCsv',
            station=f'{self.settings.meta_url}/resources/stations/{site.name}',
            order_by={"prop": "timeEnd", "descending": True},
            limit=1
        )

        if len(response_from_icos) == 0:
            self.logger.error(f"no submissions found for {site.name}", site=site.name)
            return []

        # get first, we're only getting latest submission
        submission = response_from_icos[0]
        submission_timestamp_seconds = int(submission.submission_time.timestamp())

        if site.last_fetched is not None and submission_timestamp_seconds <= site.last_fetched:
            self.logger.warning(f"no new submissions for {site.name}", site=site.name)
            return []

        submission_object_id = parse_submission_id(submission.uri, site.name)

        self.logger.info(f"fetching file contents for submission {submission_object_id}", site=site.name, submission=submission_object_id)

        return get_file_paths_for_submission(self.settings.data_url, submission_object_id)