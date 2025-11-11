import requests
from icoscp_core.icos import meta

from src.carbon_tracking_service.core import Submission
from src.carbon_tracking_service.crosscutting import config
from src.common import logging

__all__ = ["retrieve_files", "get_all_latest"]

from src.carbon_tracking_service.infrastructure.icos import is_submission_not_found, is_submission_id_malformed, \
    parse_icos_submissions


class SubmissionMalformedException(Exception):

    def __init__(self, sub_id: str):
        super().__init__(f"Submission ID {sub_id} malformed")


class SubmissionNotFoundException(Exception):

    def __init__(self, sub_id: str):
        super().__init__(f"Submission {sub_id} not found")


def retrieve_files(submission: str) -> list[str]:
    response = requests.get(f"{config.lazy_icos_settings().data_url}/zip/{submission}/listContents")

    if is_submission_id_malformed(response):
        logging.logger.error(f"invalid submission id: {submission}")
        raise SubmissionMalformedException(submission)

    if is_submission_not_found(response, submission):
        logging.logger.error(f"no submission contents found for {submission}")
        raise SubmissionNotFoundException(submission)

    json_files = response.json()

    return [file["path"] for file in json_files if "path" in file]


def get_all_latest() -> dict[str, Submission]:
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