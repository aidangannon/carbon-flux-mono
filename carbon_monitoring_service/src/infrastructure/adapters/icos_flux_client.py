import requests
from icoscp_core.icos import meta

from carbon_monitoring_service.src.core import Submission
import carbon_monitoring_service.src.crosscutting.config as config
import carbon_monitoring_service.src.infrastructure.icos as icos
from lambda_common import logging

__all__ = ["retrieve_files", "get_all_latest"]


def retrieve_files(submission: str) -> list[str]:
    response = requests.get(f"{config.lazy_icos_settings().data_url}/zip/{submission}/listContents")

    if icos.is_submission_id_malformed(response):
        logging.logger.error(f"invalid submission id: {submission}")
        raise icos.SubmissionMalformedException(submission)

    if icos.is_submission_not_found(response, submission):
        logging.logger.error(f"no submission contents found for {submission}")
        raise icos.SubmissionNotFoundException(submission)

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

    return icos.parse_icos_submissions(response_from_icos)
