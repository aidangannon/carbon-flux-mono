python_sources(
    dependencies=[
        "src/carbon_tracking_service"
    ]
)

python_aws_lambda_function(
    name="get_latest_submissions_lambda",
    handler="src/carbon_tracking_service/entry_points/get_latest_submissions:handle",
    dependencies=[
        ":entry_points"
    ]
)

python_aws_lambda_function(
    name="get_files_for_submission_lambda",
    handler="src/carbon_tracking_service/entry_points/get_files_for_submission:handle",
    dependencies=[
        ":entry_points"
    ]
)