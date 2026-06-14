python_sources()

python_aws_lambda_function(
    name="get_latest_submissions_lambda",
    handler="carbon_monitoring_service/src/entry_points/get_latest_submissions:handle",
    dependencies=[
        ":entry_points"
    ]
)

python_aws_lambda_function(
    name="get_files_for_submission_lambda",
    handler="carbon_monitoring_service/src/entry_points/get_files_for_submission:handle",
    dependencies=[
        ":entry_points"
    ]
)
