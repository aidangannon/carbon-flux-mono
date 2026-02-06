terraform_module()

terraform_backend(
    name="backend",
    source="backend.toml",
)

terraform_deployment(
    name="deployment",
    root_module=":deploy",
    dependencies=[":backend"],
)
