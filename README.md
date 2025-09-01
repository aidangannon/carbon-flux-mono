# Carbon Flux Monitoring

Pants monorepo with 4 AWS Lambda functions for ICOS eddy covariance data processing.

## Build System

Python 3.11 + Pants 2.24.2 + `pants.backend.awslambda.python`

## Targets

```bash
pants package ::  # Build all lambdas
pants list ::     # List targets
pants test tests::    # Run tests
```

## Lambda Functions

```
src/datafetcher:lambda      # EventBridge → ICOS API → SQS
src/usermanagement:lambda   # API Gateway → DynamoDB
src/fluxprocessor:lambda    # SQS → flux calculations → DynamoDB  
src/fluxter:lambda          # EventBridge → S3 archival
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