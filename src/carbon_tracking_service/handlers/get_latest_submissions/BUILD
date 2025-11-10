python_sources(
    sources=["handler.py"],
    dependencies=[
        "//:reqs#icoscp",
        "src/carbon_tracking_service"
    ]
)

python_aws_lambda_function(
    name="get_latest_submissions_lambda",
    handler="src/carbon_tracking_service/handlers/get_latest_submissions/handler:handle",
    dependencies=[
        ":get_latest_submissions"
    ]
)