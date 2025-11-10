from dataclasses import dataclass


@dataclass(
    frozen=True,
    slots=True,
    unsafe_hash=True
)
class TrackSiteCommand:
    """
    to start tracking a site for data fetching
    """
    name: str
    user_id: str