from dataclasses import dataclass
from typing import Protocol, Optional

from src.flux_tracking_service.core import TrackedSite, FileUrl, SiteId


@dataclass(
    frozen=True,
    slots=True,
    unsafe_hash=True,
)
class FluxSubmission:
    site: SiteId
    submission: str
    submission_time: int


@dataclass(
    frozen=True,
    slots=True,
    unsafe_hash=True,
)
class Submission:
    submission: str
    submission_time: int


class GetAllTrackedSites(Protocol):

    def __call__(self) -> list[TrackedSite]:
        ...

class GetLatestSubmissionFeed(Protocol):

    def __call__(self) -> dict[str, Submission]:
        ...