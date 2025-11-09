from datetime import datetime

from icoscp_core.sparql import SparqlResults
from requests import Response

from src.flux_tracking_service.core import Submission


class SubmissionObjectIdMalformed(Exception):

    def __init__(self, uri: str):
        super().__init__(f"submission object id malformed: {uri}")

class SiteUriMalformed(Exception):

    def __init__(self, uri: str):
        super().__init__(f"site uri malformed: {uri}")


def is_submission_not_found(response: Response, submission_id: str) -> bool:
    not_found_message = f"""No metadata found for data object with SHA-256 hash of {submission_id}
se.lu.nateko.cp.data.api.MetadataObjectNotFound: No metadata found for data object with SHA-256 hash of {submission_id}
"""
    if response.status_code == 500 and response.text == not_found_message:
        return True

    return False


def is_submission_id_malformed(response: Response) -> bool:
    not_found_message = "Expected base64Url- or hex-encoded SHA-256 hash"
    if response.status_code == 400 and response.text == not_found_message:
        return True

    return False


def parse_icos_submissions(submissions: SparqlResults) -> dict[str, Submission]:
    return {
        parse_site_uri(binding["station"].uri): Submission(
            submission=parse_submission_id(binding["dobj"].uri),
            submission_time=int(datetime.fromisoformat(binding["submTime"].value).timestamp())
        )
        for binding in submissions.bindings
    }


def parse_submission_id(uri: str) -> str:
    parts = uri.split('/')

    if len(parts) < 5:
        raise SubmissionObjectIdMalformed(uri)

    return parts[4]

def parse_site_uri(uri: str) -> str:
    parts = uri.split('/')

    if len(parts) < 6:
        raise SiteUriMalformed(uri)

    return parts[5]