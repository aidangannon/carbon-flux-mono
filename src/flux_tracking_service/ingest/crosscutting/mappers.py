from typing import Optional

from src.flux_tracking_service.core import TrackedSite


def map_data_tracked_site_to_core(site: Optional[dict]) -> Optional[TrackedSite]:
    if site is None:
        return None

    return TrackedSite(
        name=site["name"],
        last_fetched=int(site["last_fetched"]) if site["last_fetched"] else None,
        enabled=True
    )

