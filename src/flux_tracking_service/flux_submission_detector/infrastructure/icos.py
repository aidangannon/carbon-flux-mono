from dataclasses import dataclass
from datetime import datetime
from string import Template

import requests
from icoscp_core.icos import meta
from icoscp_core.sparql import SparqlResults

from src.common.logging import Logger
from src.flux_tracking_service.core import TrackedSite, SiteId
from src.flux_tracking_service.flux_submission_detector.config import IcosSettings
from src.flux_tracking_service.flux_submission_detector.core import FileUrl, Submission


def parse_icos_submissions(submissions: SparqlResults) -> dict[str ,Submission]:
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


def get_file_paths_for_submission(api_url: str, submission_id: str):
    content_response = requests.get(f"{api_url}/zip/{submission_id}/listContents")
    json_files = content_response.json()

    return [file["path"] for file in json_files if "path" in file]


class SubmissionObjectIdMalformed(Exception):

    def __init__(self, uri: str):
        super().__init__(f"submission object id malformed: {uri}")

class SiteUriMalformed(Exception):

    def __init__(self, uri: str):
        super().__init__(f"site uri malformed: {uri}")

@dataclass(frozen=True, slots=True)
class IcosGetLatestSubmissionFeed:
    settings: IcosSettings

    def __call__(self) -> dict[str, Submission]:
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