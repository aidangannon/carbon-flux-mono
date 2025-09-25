import uuid
from datetime import datetime
from string import Template

from responses import RequestsMock, POST, matchers, GET

SESSION_ID = str(uuid.uuid4())

META_URL = "https://meta.icos-cp.eu"
DATA_URL = "http://data.icos-cp.eu"
META_URL_NON_HTTPS = "http://meta.icos-cp.eu"
SPARQL_PATH = f"{META_URL}/sparql"


def configure_get_etc_submissions_with_latest(
    station: str,
    datatype: str,
    order_desc_field: str,
    submission_object: str,
    limit: int,
    submission_time: datetime,
    request_mock: RequestsMock
):
    configure_get_etc_submissions_with_bindings(
        station=station,
        datatype=datatype,
        order_desc_field=order_desc_field,
        bindings=[
            {
                "dobj": {
                    "type": "uri",
                    "value": f"https://meta.icos-cp.eu/objects/{submission_object}"
                },
                "spec": {
                    "type": "uri",
                    "value": "http://meta.icos-cp.eu/resources/cpmeta/etcEddyFluxRawSeriesCsv"
                },
                "station": {
                    "type": "uri",
                    "value": "http://meta.icos-cp.eu/resources/stations/ES_FR-FBn"
                },
                "fileName": {
                    "type": "literal",
                    "value": "FR-FBn_EC_20250917_L05_F01.zip"
                },
                "size": {
                    "datatype": "http://www.w3.org/2001/XMLSchema#long",
                    "type": "literal",
                    "value": "96346190"
                },
                "submTime": {
                    "datatype": "http://www.w3.org/2001/XMLSchema#dateTime",
                    "type": "literal",
                    "value": submission_time \
                        .isoformat() \
                        .replace("+00:00", "Z")
                },
                "timeStart": {
                    "datatype": "http://www.w3.org/2001/XMLSchema#dateTime",
                    "type": "literal",
                    "value": "2025-09-16T23:00:00Z"
                },
                "timeEnd": {
                    "datatype": "http://www.w3.org/2001/XMLSchema#dateTime",
                    "type": "literal",
                    "value": "2025-09-17T23:00:00Z"
                }
            }
        ],
        limit=limit,
        request_mock=request_mock,
    )


def configure_get_etc_submissions_with_bindings(
    station: str,
    datatype: str,
    order_desc_field: str,
    bindings: list[dict],
    limit: int,
    request_mock: RequestsMock
):
    request = Template("""
prefix cpmeta: <http://meta.icos-cp.eu/ontologies/cpmeta/>
prefix prov: <http://www.w3.org/ns/prov#>
prefix xsd: <http://www.w3.org/2001/XMLSchema#>
select ?dobj ?spec ?station ?samplingHeight ?fileName ?size ?submTime ?timeStart ?timeEnd
where {
	VALUES ?spec { <http://meta.icos-cp.eu/resources/cpmeta/${datatype}> }
	?dobj cpmeta:hasObjectSpec ?spec .
	VALUES ?station { <http://meta.icos-cp.eu/resources/stations/${station}> }
	?dobj cpmeta:wasAcquiredBy/prov:wasAssociatedWith ?station .
	OPTIONAL{ ?dobj cpmeta:wasAcquiredBy/cpmeta:hasSamplingHeight ?samplingHeight . }
	?dobj cpmeta:hasSizeInBytes ?size .
	?dobj cpmeta:hasName ?fileName .
	?dobj cpmeta:wasSubmittedBy/prov:endedAtTime ?submTime .
	?dobj cpmeta:hasStartTime | (cpmeta:wasAcquiredBy / prov:startedAtTime) ?timeStart .
	?dobj cpmeta:hasEndTime | (cpmeta:wasAcquiredBy / prov:endedAtTime) ?timeEnd .
	FILTER NOT EXISTS {[] cpmeta:isNextVersionOf ?dobj}
\t
}
order by desc(?${order_desc_param})
offset 0 limit ${limit}""")
    request_body = request.substitute(
        datatype=datatype,
        station=station,
        order_desc_param=order_desc_field,
        limit=limit
    )
    request_mock.add(
        method=POST,
        url=SPARQL_PATH,
        json={
            "head": {
                "vars": [
                    "dobj",
                    "spec",
                    "station",
                    "samplingHeight",
                    "fileName",
                    "size",
                    "submTime",
                    "timeStart",
                    "timeEnd"
                ]
            },
            "results": {
                "bindings": bindings
            }
        },
        match=[matchers.body_matcher(request_body)]
    )


def configure_get_content(
    submission_object: str,
    file_urls: list[str],
    request_mock: RequestsMock
):
    response = [
        {
            "name": "FR-FBn_EC_202509120030_L05_F01.zip",
            "path": file_url,
            "size": 12321321
        }
        for file_url in file_urls
    ]

    request_mock.add(
        method=GET,
        url=f"{DATA_URL}/zip/{submission_object}/listContents",
        json=response
    )