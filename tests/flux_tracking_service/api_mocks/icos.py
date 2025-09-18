from string import Template

from responses import RequestsMock, POST


META_BASE_URL = "https://meta.test-icos.py"
SPARQL_PATH = f"{META_BASE_URL}/sparql"


def configure_get_submissions(
    station: str,
    datatype: str,
    order_desc_field: str,
    submission_object: str,
    limit: int,
    request_mock: RequestsMock
):
    request = Template("""
prefix cpmeta: <http://meta.icos-cp.eu/ontologies/cpmeta/>
prefix prov: <http://www.w3.org/ns/prov#>
prefix xsd: <http://www.w3.org/2001/XMLSchema#>


select ?dobj ?spec ?station ?samplingHeight ?fileName ?size ?submTime ?timeStart ?timeEnd
where {
	VALUES ?spec { <http://meta.icos-cp.eu/resources/cpmeta/$datatype> }
	?dobj cpmeta:hasObjectSpec ?spec .
	VALUES ?station { <http://meta.icos-cp.eu/resources/stations/$station> }
	?dobj cpmeta:wasAcquiredBy/prov:wasAssociatedWith ?station .
	OPTIONAL{ ?dobj cpmeta:wasAcquiredBy/cpmeta:hasSamplingHeight ?samplingHeight . }
	?dobj cpmeta:hasSizeInBytes ?size .
	?dobj cpmeta:hasName ?fileName .
	?dobj cpmeta:wasSubmittedBy/prov:endedAtTime ?submTime .
	?dobj cpmeta:hasStartTime | (cpmeta:wasAcquiredBy / prov:startedAtTime) ?timeStart .
	?dobj cpmeta:hasEndTime | (cpmeta:wasAcquiredBy / prov:endedAtTime) ?timeEnd .
	FILTER NOT EXISTS {[] cpmeta:isNextVersionOf ?dobj}
	
	
}
order by desc(?order_desc_param)
offset 0 limit $limit
        """)
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
                "bindings": [
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
                            "value": "2025-09-18T01:23:06.347Z"
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
                ]
            }
        },
        body=request.substitute(
            datatype=datatype,
            station=station,
            order_desc_param=order_desc_field,
            limit=limit
        )
    )