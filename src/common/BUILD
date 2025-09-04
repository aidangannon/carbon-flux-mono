python_sources(
    dependencies=[
        "//:reqs#punq",
        "//:reqs#loguru"
    ]
)

python_aws_lambda_layer(
    name="layer",
    dependencies=[":common"],
    description="Flux Common",
    runtime="python3.11"
)