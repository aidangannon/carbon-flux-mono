python_sources()

python_sources(
    name="icos_config",
    sources=[
        ".icoscp/config.json"
    ]
)

python_aws_lambda_function(
    name="lambda",
    handler="src/fluxter_scrape/handler:handle",
    dependencies=[
        ":fluxter_scrape",
        ":icos_config",
        "//:reqs#icoscp"
    ]
)