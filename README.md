# Carbon Flux Monitoring

Pants monorepo with 4 AWS Lambda functions for ICOS eddy covariance data processing.

## Features

### BDD-style Integration Tests

```python
def test(get_item_feature):
    get_item_feature.runner
        .given(data_exists_in_the_db)
        .when(lambda_is_called_with_data_id)
        .then(lambda_response_should_equal_data)
        .assert_all()
```

### LRU-cached IoC Container
```python
@lru_cache(maxsize=1)
def get_container(ioc_registrar: IocHandle) -> Container:
    container = Container()
    ioc_registrar(container)
    return container  # Cached across Lambda warm invocations
```

### Lambda Handler Factory
```python
handle = lazy_handler_factory(
    inner_handler=inner_handle,
    ioc_registrar=bootstrap
)
```

### Terraform Infrastructure
```hcl
resource "aws_lambda_function" "fluxter_scrape" {
  function_name = "flux_tracking_service-scrape"
  layers        = [aws_lambda_layer_version.common.arn]
  
  depends_on = [aws_dynamodb_table.fluxter_db]
}
```

### Common Lambda Layer
```python
# src/common/handlers.py - Shared across all lambdas
# src/common/logging.py  - Centralized logging
# Packaged as reusable Lambda layer
```

## Build System

Python 3.11 + Pants 2.24.2 + `pants.backend.awslambda.python`

```bash
pants package ::     # Build all lambdas
pants test ::        # Run BDD integration tests
pants list ::        # List targets
```

## Lambda Functions

```
src/datafetcher:lambda      # EventBridge → ICOS API → SQS
src/usermanagement:lambda   # API Gateway → DynamoDB
src/fluxprocessor:lambda    # SQS → flux calculations → DynamoDB  
src/fluxter_scrape:lambda   # DynamoDB item retrieval
```

## Dependencies

```bash
# Add dependency  
echo "requests==2.31.0" >> requirements.txt
pants generate-lockfiles --resolve=python-default

# Reference in BUILD
python_sources(dependencies=["//:reqs#requests"])
```

## BUILD Files

```python
# Lambda function target
python_aws_lambda_function(
    name="lambda",
    handler="handler:handle", 
    dependencies=[":sources", "//src/common"]
)

# Sources target
python_sources()
```

## Project Structure

```
BUILD                       # Root python_requirements()
requirements.txt            # Dependency versions
python-default.lock         # Generated lockfile
pants.toml                  # Pants configuration
src/
  common/BUILD              # Shared dependencies
  {service}/
    BUILD                   # Lambda + sources targets
    handler.py             # Lambda entry point
```

## CI/CD

GitHub Actions + `pantsbuild/actions/init-pants@v8`

```yaml
- uses: pantsbuild/actions/init-pants@v8
- run: pants run tests:unittest_runner
- run: pants package ::
```