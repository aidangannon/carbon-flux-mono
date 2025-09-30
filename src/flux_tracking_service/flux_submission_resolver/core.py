from typing import Protocol


class RetrieveFilesForSubmission(Protocol):

    def __call__(self, submission: str) -> list[str]:
        ...