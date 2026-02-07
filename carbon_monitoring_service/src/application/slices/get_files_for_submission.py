import carbon_monitoring_service.src.application.ports as ports


def get(
    site: str,
    submission: str,
    submission_timestamp: int,
) -> list[str]:
    files = ports.flux_client.retrieve_files(submission)

    if len(files) == 0:
        return []

    ports.monitored_site_repository.update_last_fetched(site, submission_timestamp)

    return files
