from typing import Protocol


class RetrieveFilesForSubmission(Protocol):

    def __call__(self, submission: str) -> list[str]:
        ...

class UpdateSiteLastFetched(Protocol):

    def __call__(self, site: str, submission_timestamp: int) -> None:
        ...