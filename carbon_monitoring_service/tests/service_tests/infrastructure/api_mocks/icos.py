import uuid
from dataclasses import dataclass
from datetime import datetime
from string import Template

from responses import RequestsMock, POST, matchers, GET

SESSION_ID = str(uuid.uuid4())

META_URL = "https://meta.icos-cp.eu"
DATA_URL = "https://data.icos-cp.eu"
SPARQL_PATH = f"{META_URL}/sparql"


@dataclass
class Submission:
    id: str
    submission_time: datetime


def create_binding(site: str, submission_time: datetime, dobj_uri: str) -> dict:
    return {
        "dobj": {"type": "uri", "value": dobj_uri},
        "submTime": {
            "datatype": "http://www.w3.org/2001/XMLSchema#dateTime",
            "type": "literal",
            "value": submission_time.isoformat().replace("+00:00", "Z"),
        },
        "station": {
            "type": "uri",
            "value": f"http://meta.icos-cp.eu/resources/stations/{site}",
        },
    }


def configure_get_etc_submissions_with_latest(
    datatype: str, submissions: dict[str, Submission], request_mock: RequestsMock
):

    configure_get_etc_submissions_with_bindings(
        datatype=datatype,
        bindings=[
            create_binding(
                site,
                submission.submission_time,
                f"https://meta.icos-cp.eu/objects/{submission.id}",
            )
            for site, submission in submissions.items()
        ],
        request_mock=request_mock,
    )


def configure_get_etc_submissions_with_invalid_submission_id(
    datatype: str, site: str, submission_time: datetime, request_mock: RequestsMock
):
    configure_get_etc_submissions_with_bindings(
        datatype=datatype,
        bindings=[create_binding(site, submission_time, "invalid_unparsable")],
        request_mock=request_mock,
    )


def configure_get_etc_submissions_with_bindings(
    datatype: str, bindings: list[dict], request_mock: RequestsMock
):
    request = Template("""
prefix cpmeta: <http://meta.icos-cp.eu/ontologies/cpmeta/>
prefix prov: <http://www.w3.org/ns/prov#>
prefix xsd: <http://www.w3.org/2001/XMLSchema#>

select ?dobj ?submTime ?station where {
    ?dobj cpmeta:hasObjectSpec <http://meta.icos-cp.eu/resources/cpmeta/${datatype}> .
    ?dobj cpmeta:wasAcquiredBy/prov:wasAssociatedWith ?station .
    ?dobj cpmeta:wasSubmittedBy/prov:endedAtTime ?submTime .
    FILTER NOT EXISTS {[] cpmeta:isNextVersionOf ?dobj}

    {
        select ?station (max(?maxSubmTime) as ?latestSubmTime) where {
            ?anyDobj cpmeta:hasObjectSpec <http://meta.icos-cp.eu/resources/cpmeta/${datatype}> .
            ?anyDobj cpmeta:wasAcquiredBy/prov:wasAssociatedWith ?station .
            ?anyDobj cpmeta:wasSubmittedBy/prov:endedAtTime ?maxSubmTime .
            FILTER NOT EXISTS {[] cpmeta:isNextVersionOf ?anyDobj}
        }
        group by ?station
    }

    FILTER(?submTime = ?latestSubmTime)
}
order by desc(?submTime)""")
    request_body = request.substitute(datatype=datatype)
    request_mock.add(
        method=POST,
        url=SPARQL_PATH,
        json={
            "head": {"vars": ["dobj", "submTime"]},
            "results": {"bindings": bindings},
        },
        match=[matchers.body_matcher(request_body)],
    )


def configure_get_content(
    submission_object: str, file_urls: list[str], request_mock: RequestsMock
):
    response = [
        {
            "name": "FR-FBn_EC_202509120030_L05_F01.zip",
            "path": file_url,
            "size": 12321321,
        }
        for file_url in file_urls
    ]

    request_mock.add(
        method=GET,
        url=f"{DATA_URL}/zip/{submission_object}/listContents",
        json=response,
    )


def configure_get_content_with_string(
    submission_object: str, body: str, request_mock: RequestsMock, status: int
):
    request_mock.add(
        method=GET,
        url=f"{DATA_URL}/zip/{submission_object}/listContents",
        body=body,
        status=status,
    )
