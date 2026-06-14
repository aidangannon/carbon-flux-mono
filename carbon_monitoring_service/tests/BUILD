python_sources(
    sources=["**/*.py"]
)

python_tests(
    name="test_suite",
    dependencies=[
        "carbon_monitoring_service/src/entry_points",
    ],
    sources=[
        "**/*_feature.py",
        "**/*_tests.py"
    ]
)
