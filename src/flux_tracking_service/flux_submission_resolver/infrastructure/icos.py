from dataclasses import dataclass

import requests
from requests import Response

from src.common.logging import Logger
from src.flux_tracking_service.flux_submission_resolver.config import IcosSettings

def is_submission_not_found(response: Response, submission_id: str) -> bool:
    not_found_message = f"""No metadata found for data object with SHA-256 hash of {submission_id}
se.lu.nateko.cp.data.api.MetadataObjectNotFound: No metadata found for data object with SHA-256 hash of {submission_id}
"""
    if response.status_code == 500 and response.text == not_found_message:
        return True

    return False


@dataclass(frozen=True, slots=True)
class IcosRetrieveFilesForSubmission:
    settings: IcosSettings
    logger: Logger

    def __call__(self, submission: str) -> list[str]:
        response = requests.get(f"{self.settings.data_url}/zip/{submission}/listContents")

        if is_submission_not_found(response, submission):
            self.logger.error(f"no submission contents found for {submission}")

        return []