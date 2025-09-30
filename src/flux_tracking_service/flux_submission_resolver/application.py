from dataclasses import dataclass

from src.common.logging import Logger
from src.flux_tracking_service.flux_submission_resolver.core import RetrieveFilesForSubmission


@dataclass(slots=True, frozen=True)
class ResolveFilesForSubmission:
    logger: Logger
    retrieve_files_for_submission: RetrieveFilesForSubmission

    def __call__(self, submission: str) -> list[str]:
        self.retrieve_files_for_submission(submission)

        return []