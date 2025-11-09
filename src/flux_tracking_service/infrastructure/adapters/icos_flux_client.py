from dataclasses import dataclass
from datetime import datetime

import requests
from icoscp_core.icos import meta
from icoscp_core.sparql import SparqlResults
from requests import Response

from src.common import logging
from src.flux_tracking_service.core import Submission
from src.flux_tracking_service.crosscutting import config

__all__ = ["retrieve_files", "get_all_latest"]

from src.flux_tracking_service.infrastructure.icos import is_submission_not_found, is_submission_id_malformed, \
    parse_icos_submissions


def retrieve_files(submission: str) -> list[str]:
    response = requests.get(f"{config.icos_settings.data_url}/zip/{submission}/listContents")

    if is_submission_id_malformed(response):
        logging.logger.error(f"invalid submission id: {submission}")

    if is_submission_not_found(response, submission):
        logging.logger.error(f"no submission contents found for {submission}")

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