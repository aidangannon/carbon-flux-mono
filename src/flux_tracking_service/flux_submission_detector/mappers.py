from typing import Optional

from src.flux_tracking_service.core import TrackedSite
from src.flux_tracking_service.flux_submission_detector.core import FluxSubmission


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

def map_core_flux_submission_to_response(flux_submission: Optional[FluxSubmission]) -> Optional[dict]:
    if flux_submission is None:
        return None

    return {
        "site": flux_submission.site,
        "submission": flux_submission.submission,
        "submission_time": flux_submission.submission_time
    }

def map_core_flux_submissions_to_responses(flux_submissions: Optional[list[FluxSubmission]]) -> Optional[list[dict]]:
    if flux_submissions is None:
        return None

    return [map_core_flux_submission_to_response(flux_submission) for flux_submission in flux_submissions]