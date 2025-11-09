from src.flux_tracking_service.application import ports


def execute(
    site: str,
    submission: str,
    submission_timestamp: int,
    submission_client: ports.FluxClient,
    tracked_site_repo: ports.TrackedSiteRepository
) -> list[str]:
    submission_client.retrieve_files(submission)

    tracked_site_repo.update_last_fetched(site, submission_timestamp)

    return []