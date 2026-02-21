from dataclasses import dataclass


@dataclass(frozen=True, slots=True, unsafe_hash=True)
class MonitorSiteCommand:
    """
    to start monitoring a site for data fetching
    """

    name: str
    user_id: str
