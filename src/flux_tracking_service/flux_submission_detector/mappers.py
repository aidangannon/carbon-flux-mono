from typing import Optional

from src.flux_tracking_service.core import TrackedSite
from src.flux_tracking_service.flux_submission_detector.core import FluxSubmission


def map_data_tracked_site_to_core(site: dict | None) -> TrackedSite | None:
    if site is None:
        return None

    return TrackedSite(
        name=site["name"],
        last_fetched=int(site["last_fetched"]) if site["last_fetched"] else None,
        enabled=True
    )

def map_data_tracked_sites_to_core_tracked_sites(sites: list[dict] | None) -> list[TrackedSite] | None:
    if sites is None:
        return None

    return [map_data_tracked_site_to_core(site) for site in sites]

def map_core_flux_submission_to_response(flux_submission: FluxSubmission | None) -> dict | None:
    if flux_submission is None:
        return None

    return {
        "site": flux_submission.site,
        "submission": flux_submission.submission,
        "submission_time": flux_submission.submission_time
    }

def map_core_flux_submissions_to_responses(flux_submissions: list[FluxSubmission] | None) -> list[dict] | None:
    if flux_submissions is None:
        return None

    return [map_core_flux_submission_to_response(flux_submission) for flux_submission in flux_submissions]