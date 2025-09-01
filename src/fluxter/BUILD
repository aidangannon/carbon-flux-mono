python_sources()

python_aws_lambda_function(
    name="lambda",
    handler="src/fluxter/handler:handle",
    dependencies=[
        ":fluxter",
        "src/common"
    ]
)