from dataclasses import dataclass

from src.flux_tracking_service.ingest.core import FileUrl


@dataclass(frozen=True, slots=True)
class Submission:
    submission_id: str
    file_urls: list[FileUrl]
