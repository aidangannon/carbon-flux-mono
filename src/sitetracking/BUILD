python_sources()

python_aws_lambda_function(
    name="lambda",
    handler="src/sitetracking/handler:handle",
    dependencies=[
        ":sitetracking",
        "src/common"
    ]
)