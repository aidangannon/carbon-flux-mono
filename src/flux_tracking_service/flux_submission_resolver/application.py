from dataclasses import dataclass

from src.common.logging import Logger
from src.flux_tracking_service.flux_submission_resolver.core import RetrieveFilesForSubmission, UpdateSiteLastFetched


@dataclass(slots=True, frozen=True)
class ResolveFilesForSubmission:
    logger: Logger
    retrieve_files_for_submission: RetrieveFilesForSubmission
    update_last_fetched: UpdateSiteLastFetched

    def __call__(self, site: str, submission: str, submission_timestamp: int) -> list[str]:
        self.retrieve_files_for_submission(submission)

        self.update_last_fetched(site, submission_timestamp)

        return []