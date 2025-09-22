# Carbon Flux Monitoring

A serverless monorepo for processing ICOS (Integrated Carbon Observation System) eddy covariance data using AWS Step Functions and Lambda microservices. Built with Pants build system for scalable carbon flux data monitoring and analysis.

## Features

### BDD-style Integration Tests

```python
@scenario
def test_when_no_submissions_are_available_for_site(retrieve_flux_submissions_feature):
    ctx = retrieve_flux_submissions_feature
    ctx.runner \
        .given(a_tracked_site_is_added_with_last_fetched_LAST_FETCHED(ctx)) \
        .and_also(icos_api_is_configured_with_station_STATION_ID_to_return_empty(ctx.station_id, ctx.requests_mock)) \
        .when(lambda_is_invoked(ctx)) \
        .then(result_is_empty(ctx)) \
        .run_all_steps()
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

## Architecture

### Microservices

**Flux Tracking Service** - Scientific site monitoring and data ingestion
- **Ingest Lambda**: EventBridge-triggered ICOS API data collection
- **Processing Pipeline**: Step Functions orchestrating multiple data processing Lambdas
- **Data Storage**: DynamoDB for site tracking, S3 for flux measurements

**Flux Management Service** - Data analysis and workflow management
- **API Gateway**: RESTful endpoints for data access and management
- **Calculation Engine**: Step Functions coordinating flux analysis workflows
- **Data Processing**: Multiple specialized Lambdas for different calculation types

### Data Flow

```
EventBridge (hourly) → Ingest Lambda → Step Functions
                                    ↓
                              Processing Lambdas (parallel)
                                    ↓
                            DynamoDB + S3 Storage
```

Each ingest operation triggers a Step Function that executes multiple processing Lambdas in parallel for efficient data analysis and storage.

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
carbon-flux-mono/
├── src/
│   ├── common/                    # Shared Lambda layer
│   │   ├── handlers.py           # Common handler utilities
│   │   ├── logging.py            # Centralized logging setup
│   │   └── BUILD                 # Layer packaging config
│   ├── flux_tracking_service/    # Primary microservice
│   │   ├── core.py              # Domain models (TrackedSite)
│   │   ├── data.py              # DynamoDB data access
│   │   ├── events.py            # Event commands
│   │   ├── ingest/              # Data ingestion Lambda
│   │   │   ├── handler.py       # Lambda entry point
│   │   │   ├── config.py        # ICOS API configuration
│   │   │   └── bootstrap.py     # IoC container setup
│   │   └── BUILD                # Service build targets
│   └── flux_management_service/  # Secondary microservice (planned)
├── tests/                        # BDD-style integration tests
│   ├── __init__.py              # Custom BDD testing framework
│   └── flux_tracking_service/   # Service-specific tests
├── BUILD                         # Root python_requirements()
├── requirements.txt              # Dependency versions
├── python-default.lock          # Generated lockfile
└── pants.toml                   # Pants build configuration
```

### Key Technologies

- **Python 3.11** with type hints and dataclasses
- **ICOS Carbon Portal** (`icoscp`) for scientific data access
- **AWS SDK** (`boto3`) with type stubs for development
- **Dependency Injection** (`punq`) for clean architecture
- **Structured Logging** (`loguru`) for observability
- **Property-Based Testing** (`hypothesis`) for robust test data

## CI/CD

GitHub Actions + `pantsbuild/actions/init-pants@v8`

```yaml
- uses: pantsbuild/actions/init-pants@v8
- run: pants run tests:unittest_runner
- run: pants package ::
```