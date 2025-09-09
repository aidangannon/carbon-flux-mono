python_sources()

python_tests(
    name="test_suite",
    dependencies=[
        "src/fluxter_scrape",
        "src/common",
        "//:reqs#assertpy",
        "//:reqs#moto",
        "//:reqs#pytest"
    ],
    sources=[
        "**/*_test.py"
    ]
)

python_test_utils(
    name="test_utils",
    sources=[
        "**/conftest.py"
    ]
)