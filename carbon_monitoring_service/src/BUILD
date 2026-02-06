python_sources(
    sources=["**/*.py", "!contracts.py"],
    dependencies=[
        "lambda_common",
        ":carbon_monitoring_contracts",
        "//:reqs#icoscp"
    ]
)

python_sources(
    name="carbon_monitoring_contracts",
    sources=["contracts.py"]
)
