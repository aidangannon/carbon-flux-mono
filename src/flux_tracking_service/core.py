from dataclasses import dataclass
from typing import Protocol

@dataclass(
    frozen=True,
    slots=True,
    unsafe_hash=True
)
class TrackedSite:
    """
    used for keeping track of which sites we need to pull data for
    """
    id: str
    name: str
    user_id: str
    enabled: bool


class GetAllTrackedSites(Protocol):

    def __call__(self) -> list[TrackedSite]:
        ...