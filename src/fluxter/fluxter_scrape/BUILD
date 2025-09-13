python_sources()

python_aws_lambda_function(
    name="lambda",
    handler="src/fluxter/fluxter_scrape/handler:handle",
    dependencies=[
        ":fluxter_scrape",
        "src/fluxter/fluxter_common"
        "//:reqs#icoscp"
    ]
)