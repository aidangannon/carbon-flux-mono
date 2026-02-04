python_sources(
    dependencies=[
        "//:reqs#loguru",
        "//:reqs#boto3-stubs"
    ]
)

python_aws_lambda_layer(
    name="common_layer",
    dependencies=[":common"],
    description="Flux Common",
    runtime="python3.13"
)
