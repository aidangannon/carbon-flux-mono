python_aws_lambda_function(
    sources=["get_latest_submissions.py"],
    name="get_latest_submissions_lambda",
    handler="src/carbon_tracking_service/entry_points/get_latest_submissions:handle",
    dependencies=[
        ":get_latest_submissions"
    ]
)

python_aws_lambda_function(
    sources=["get_files_for_submission.py"],
    name="get_files_for_submission_lambda",
    handler="src/carbon_tracking_service/entry_points/get_files_for_submission:handle",
    dependencies=[
        ":get_files_for_submission"
    ]
)