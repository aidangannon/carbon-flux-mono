python_sources(
    name="layer_deps",
    dependencies=[
        "//:reqs#punq",
        "//:reqs#structlog"
    ]
)

python_aws_lambda_layer(
    name="core",
    dependencies=[":layer_deps"],
    description="Common Python libraries",
    compatible_runtimes=["python3.11"]
)