python_sources(
    sources=["**/*.py", "!entry_points/**"],
    dependencies=[
        ":carbon_tracking_service",
        "src/common",
        "//:reqs#icoscp"
    ]
)

python_sources(
    name="carbon_tracking_events",
    sources=["events.py"]
)