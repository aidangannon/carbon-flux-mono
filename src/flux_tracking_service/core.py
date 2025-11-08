from dataclasses import dataclass

from src.common import UnixSeconds

FileUrl = str
SiteId = str

@dataclass(
    frozen=True,
    slots=True,
    unsafe_hash=True
)
class TrackedSite:
    """
    used for keeping track of which sites we need to pull data for
    """
    name: SiteId
    enabled: bool
    last_fetched: UnixSeconds | None = None

OPERATION = "operation"
DETECT_SUBMISSIONS = "detect_submissions"
RESOLVE_SUBMISSIONS = "resolve_submissions"