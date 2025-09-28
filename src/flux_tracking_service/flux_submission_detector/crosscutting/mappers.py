from typing import Optional

from src.flux_tracking_service.core import TrackedSite
from src.flux_tracking_service.flux_submission_detector.core import FluxFile


def map_data_tracked_site_to_core(site: Optional[dict]) -> Optional[TrackedSite]:
    if site is None:
        return None

    return TrackedSite(
        name=site["name"],
        last_fetched=int(site["last_fetched"]) if site["last_fetched"] else None,
        enabled=True
    )

def map_data_tracked_sites_to_core_tracked_sites(sites: Optional[list[dict]]) -> Optional[list[TrackedSite]]:
    if sites is None:
        return None

    return [map_data_tracked_site_to_core(site) for site in sites]

def map_core_flux_file_to_response(flux_file: Optional[FluxFile]) -> Optional[dict]:
    if flux_file is None:
        return None

    return {
        "site": flux_file.site,
        "file_url": flux_file.file
    }

def map_core_flux_files_to_responses(flux_files: Optional[list[FluxFile]]) -> Optional[list[dict]]:
    if flux_files is None:
        return None

    return [map_core_flux_file_to_response(flux_file) for flux_file in flux_files]