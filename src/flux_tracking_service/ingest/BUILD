python_sources(
    sources=["ingest/**/*.py"],
    dependencies=[
        "//:reqs#icoscp",
        "src/flux_tracking_service"
    ]
)

python_aws_lambda_function(
    name="lambda",
    handler="src/flux_tracking_service/ingest/handler:handle",
    dependencies=[
        ":ingest"
    ]
)