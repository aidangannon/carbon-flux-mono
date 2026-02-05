from dataclasses import dataclass
from typing import Protocol

from carbon_tracking_service.src.core import TrackedSite, Submission


__all__ = ["TrackedSite", "FluxClient"]


class TrackedSiteRepository(Protocol):

    def update_last_fetched(self, site: str, submission_timestamp: int) -> None:
        ...

    def get_all(self) -> list[TrackedSite]:
        ...


class FluxClient(Protocol):

    def get_all_latest(self) -> dict[str, Submission]:
        ...

    def retrieve_files(self, submission: str) -> list[str]:
        ...

@dataclass(slots=True)
class SubmissionsFacade:
    client: FluxClient
    repo: TrackedSiteRepository
