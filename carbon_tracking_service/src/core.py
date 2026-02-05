from dataclasses import dataclass

from lambda_common import UnixSeconds

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
    last_fetched: UnixSeconds | None



@dataclass(
    frozen=True,
    slots=True,
    unsafe_hash=True,
)
class Submission:
    """
    flux submission identifier and time
    """

    submission: str
    submission_time: int


@dataclass(
    frozen=True,
    slots=True,
    unsafe_hash=True,
)
class SiteSubmission:
    """
    flux submission for a particular site
    """

    site: SiteId
    submission: str
    submission_time: int
