python_sources()

python_aws_lambda_function(
    name="lambda",
    handler="src/flux_tracking_service/ingest/handler:handle",
    dependencies=[
        ":ingest",
        "src/flux_tracking_service",
        "//:reqs#icoscp"
    ]
)