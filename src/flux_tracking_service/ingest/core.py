from dataclasses import dataclass
from typing import Protocol

from src.flux_tracking_service.core import TrackedSite, FileUrl, SiteId


@dataclass(frozen=True, slots=True)
class FluxFile:
    site: SiteId
    file: FileUrl


class GetAllTrackedSites(Protocol):

    def __call__(self) -> list[TrackedSite]:
        ...

class GetFileUrlsForSite(Protocol):

    def __call__(self, site: TrackedSite) -> list[FileUrl]:
        ...