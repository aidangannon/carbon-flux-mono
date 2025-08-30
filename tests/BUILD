python_sources()

python_tests(
    name="test_suite",
    dependencies=[
        "src/sitetracking:lambda"
    ]
)

pex_binary(
    name="unittest_runner",
    entry_point="unittest",
    dependencies=[":test_suite"]
)