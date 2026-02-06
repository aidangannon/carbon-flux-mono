terraform_module()

terraform_backend(
    name="backend",
    source="backend.toml",
)

terraform_deployment(
    name="deployment",
    root_module=":deploy",
    dependencies=[
        ":backend",
        "carbon_monitoring_service/src/entry_points:get_latest_submissions_lambda",
        "carbon_monitoring_service/src/entry_points:get_files_for_submission_lambda",
    ],
)
