![Logo](/assets/logo.jpg)

# Carbon Flux Monitoring

A serverless monorepo for processing ICOS (Integrated Carbon Observation System) eddy covariance data using AWS Step Functions and Lambda microservices. Built with Pants build system for scalable carbon flux data monitoring and analysis.

## Features

### BDD-style Integration Tests

```python
@scenario
def test_when_no_submissions_are_available_for_site(retrieve_flux_submissions_feature):
    ctx = retrieve_flux_submissions_feature
    ctx.runner
    .given(a_tracked_site_is_added_with_last_fetched_LAST_FETCHED(ctx))
    .and_also(icos_api_is_configured_with_station_STATION_ID_to_return_empty(ctx.site, ctx.requests_mock))
    .when(lambda_is_invoked(ctx))
    .then(result_is_empty(ctx))
    .run_all_steps()
```

#### Test Isolation Strategy

- **Session-scoped fixtures**: DynamoDB table creation (expensive operations)
- **Function-scoped fixtures**: HTTP request mocking via `responses` library
- **Test data isolation**: Dynamic partition key prefixing with test IDs
- **Request header isolation**: Patched requests with unique test headers per test

```python
# Session scope for expensive resources
@fixture(scope='session')
def database():
    with mock_aws():
        yield dynamodb.create_table(...)

# Function scope for lightweight mocking
@fixture
def api_mocks():
    with responses.RequestsMock() as requests_mock:
        yield requests_mock
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
- **flux-site-tracker**: Handles SQS `trackedsiteadded` events, adds new tracking sites to DynamoDB
- **flux-submission-detector**: Compares ICOS feed with tracked site timestamps to identify new submissions
- **flux-submission-resolver**: Fetches file URLs from submission objects and updates tracked site timestamps
- **flux-file-processor**: Downloads and processes individual files, emits SQS events for downstream processing
- **flux-ingestion-pipeline**: Step Function orchestrating detector → resolver → processor workflow

**Flux Management Service** - Data analysis and workflow management
- **API Gateway**: RESTful endpoints for data access and management
- **Calculation Engine**: Step Functions coordinating flux analysis workflows
- **Data Processing**: Multiple specialized Lambdas for different calculation types

### Data Flow

#### Site Tracking Flow
```
SQS trackedsiteadded → flux-site-tracker → DynamoDB (tracked sites)
```

#### Ingestion Pipeline Flow
```
EventBridge (scheduled) → flux-ingestion-pipeline Step Function
                                    ↓
1. flux-submission-detector: Query tracked sites + ICOS API
                                    ↓
   Output: [{submission_obj, submission_time, site_id}, ...]
                                    ↓
2. flux-submission-resolver: Fetch file URLs + Update timestamps
                                    ↓
   Output: [{site_id, file_url}, ...]
                                    ↓
3. flux-file-processor: Download files + Process + Emit SQS events
```

The ingestion pipeline processes multiple sites and files in parallel for efficient data collection and analysis.

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