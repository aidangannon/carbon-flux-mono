from dataclasses import dataclass


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