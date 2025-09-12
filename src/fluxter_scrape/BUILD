python_sources()

python_aws_lambda_function(
    name="lambda",
    handler="src/fluxter_scrape/handler:handle",
    dependencies=[
        ":fluxter_scrape",
        "//:reqs#icoscp"
    ]
)