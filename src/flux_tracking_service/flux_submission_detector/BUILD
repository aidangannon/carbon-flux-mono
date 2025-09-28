python_sources(
    sources=["**/*.py"],
    dependencies=[
        "//:reqs#icoscp",
        "src/flux_tracking_service"
    ]
)

python_aws_lambda_function(
    name="lambda",
    handler="src/flux_tracking_service/flux_submission_detector/handler:handle",
    dependencies=[
        ":flux_submission_detector"
    ]
)