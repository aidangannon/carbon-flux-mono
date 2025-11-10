python_sources(
    sources=["handler.py"],
    dependencies=[
        "//:reqs#icoscp",
        "src/flux_tracking_service"
    ]
)

python_aws_lambda_function(
    name="get_files_for_submission_lambda",
    handler="src/flux_tracking_service/handlers/get_files_for_submission/handler:handle",
    dependencies=[
        ":get_files_for_submission"
    ]
)