from typing import Protocol

from src.fluxter.models import TrackedSite


class GetAllTrackedSites(Protocol):

    def __call__(self) -> list[TrackedSite]:
        ...