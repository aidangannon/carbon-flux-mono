from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Submission:
    submission_id: str
    file_urls: list[str]