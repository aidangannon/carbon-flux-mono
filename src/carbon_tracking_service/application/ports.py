from typing import Protocol

from src.carbon_tracking_service.core import TrackedSite, Submission


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