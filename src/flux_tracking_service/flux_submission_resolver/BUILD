python_sources(
    sources=["**/*.py"],
    dependencies=[
        "//:reqs#icoscp",
        "src/flux_tracking_service"
    ]
)

python_aws_lambda_function(
    name="flux_submission_resolver_lambda",
    handler="src/flux_tracking_service/flux_submission_resolver/handler:handle",
    dependencies=[
        ":flux_submission_resolver"
    ]
)