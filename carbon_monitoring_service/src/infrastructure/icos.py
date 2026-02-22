import requests
from icoscp_core.icos import meta

from carbon_monitoring_service.src.core import Submission
from carbon_monitoring_service.src.crosscutting import config
from lambda_common import logging
from datetime import datetime
from typing import cast

from icoscp_core.sparql import BoundLiteral, BoundUri, SparqlResults
from requests import Response


class SubmissionMalformedException(Exception):
    def __init__(self, sub_id: str):
        super().__init__(f"Submission ID {sub_id} malformed")


class SubmissionNotFoundException(Exception):
    def __init__(self, sub_id: str):
        super().__init__(f"Submission {sub_id} not found")


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
        parse_site_uri(cast(BoundUri, binding["station"]).uri): Submission(
            submission=parse_submission_id(cast(BoundUri, binding["dobj"]).uri),
            submission_time=int(
                datetime.fromisoformat(
                    cast(BoundLiteral, binding["submTime"]).value
                ).timestamp()
            ),
        )
        for binding in submissions.bindings
    }


def parse_submission_id(uri: str) -> str:
    parts = uri.split("/")

    if len(parts) < 5:
        print("TEST TESTY TEST")
        raise SubmissionObjectIdMalformed(uri)

    return parts[4]


def parse_site_uri(uri: str) -> str:
    parts = uri.split("/")

    if len(parts) < 6:
        raise SiteUriMalformed(uri)

    return parts[5]


class IcosFluxClient:
    __slots__ = ()

    def retrieve_files(self, submission: str) -> list[str]:
        response = requests.get(
            f"{config.lazy_icos_settings().data_url}/zip/{submission}/listContents"
        )

        if is_submission_id_malformed(response):
            logging.logger.error(f"invalid submission id: {submission}")
            raise SubmissionMalformedException(submission)

        if is_submission_not_found(response, submission):
            logging.logger.error(f"no submission contents found for {submission}")
            raise SubmissionNotFoundException(submission)

        json_files = response.json()

        return [file["path"] for file in json_files if "path" in file]

    def get_all_latest(self) -> dict[str, Submission]:
        request = """
prefix cpmeta: <http://meta.icos-cp.eu/ontologies/cpmeta/>
prefix prov: <http://www.w3.org/ns/prov#>
prefix xsd: <http://www.w3.org/2001/XMLSchema#>

select ?dobj ?submTime ?station where {
    ?dobj cpmeta:hasObjectSpec <http://meta.icos-cp.eu/resources/cpmeta/etcEddyFluxRawSeriesCsv> .
    ?dobj cpmeta:wasAcquiredBy/prov:wasAssociatedWith ?station .
    ?dobj cpmeta:wasSubmittedBy/prov:endedAtTime ?submTime .
    FILTER NOT EXISTS {[] cpmeta:isNextVersionOf ?dobj}

    {
        select ?station (max(?maxSubmTime) as ?latestSubmTime) where {
            ?anyDobj cpmeta:hasObjectSpec <http://meta.icos-cp.eu/resources/cpmeta/etcEddyFluxRawSeriesCsv> .
            ?anyDobj cpmeta:wasAcquiredBy/prov:wasAssociatedWith ?station .
            ?anyDobj cpmeta:wasSubmittedBy/prov:endedAtTime ?maxSubmTime .
            FILTER NOT EXISTS {[] cpmeta:isNextVersionOf ?anyDobj}
        }
        group by ?station
    }

    FILTER(?submTime = ?latestSubmTime)
}
order by desc(?submTime)"""
        response_from_icos = meta.sparql_select(request)

        return parse_icos_submissions(response_from_icos)
