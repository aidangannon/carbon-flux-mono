from carbon_tracking_service.src.application import ports


def execute(
    site: str,
    submission: str,
    submission_timestamp: int,
    facade: ports.SubmissionsFacade
) -> list[str]:
    files = facade \
        .client \
        .retrieve_files(submission)

    if len(files) == 0:
        return []

    facade \
        .repo \
        .update_last_fetched(site, submission_timestamp)

    return files