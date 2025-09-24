from dataclasses import dataclass
from datetime import datetime
from typing import Protocol, Optional

from src.common import UnixSeconds


@dataclass(
    frozen=True,
    slots=True,
    unsafe_hash=True
)
class TrackedSite:
    """
    used for keeping track of which sites we need to pull data for
    """
    name: str
    enabled: bool
    last_fetched: Optional[UnixSeconds] = None


class GetAllTrackedSites(Protocol):

    def __call__(self) -> list[TrackedSite]:
        ...