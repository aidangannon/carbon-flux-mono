from dataclasses import dataclass

import requests

from src.flux_tracking_service.core import FileUrl


@dataclass(frozen=True, slots=True)
class Submission:
    submission_id: str
    file_urls: list[FileUrl]


def get_file_paths_for_submission(api_url: str, submission_id: str):
    content_response = requests.get(f"{api_url}/zip/{submission_id}/listContents")
    json_files = content_response.json()

    return [file["path"] for file in json_files if "path" in file]