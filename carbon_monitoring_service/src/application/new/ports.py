from dataclasses import dataclass
from typing import Protocol

from carbon_monitoring_service.src.core import MonitoredSite, Submission


__all__ = ["MonitoredSite", "FluxClient"]

class MonitoredSiteRepository(Protocol):

    def update_last_fetched(self, site: str, submission_timestamp: int) -> None:
        ...

    def get_all(self) -> list[MonitoredSite]:
        ...


class FluxClient(Protocol):

    def get_all_latest(self) -> dict[str, Submission]:
        ...

    def retrieve_files(self, submission: str) -> list[str]:
        ...

monitored_site_repository: MonitoredSiteRepository
flux_client: FluxClient
