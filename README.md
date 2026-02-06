# Carbon Flux Monitoring

![Logo](/assets/7500DS-thumb.webp)

Serverless monorepo for processing ICOS eddy covariance data with AWS Step Functions and Lambda.

## Code

### BDD Tests
```python
@scenario
def test_when_no_submissions_are_available_for_site(retrieve_flux_submissions_feature):
    ctx = retrieve_flux_submissions_feature
    ctx.runner
    .given(a_monitored_site_is_added_with_last_fetched_LAST_FETCHED(ctx))
    .when(lambda_is_invoked(ctx))
    .then(result_is_empty(ctx))
    .run_all_steps()
```

### Cached Infra
```python
@functools.lru_cache(maxsize=1)
def lazy_table() -> Table:
    return boto3 \
        .resource('dynamodb', region_name=config.lazy_dynamo_settings().region) \
        .Table(name=config.lazy_dynamo_settings().table_name)
```

## Namespaces

Packages follow a `<service>.<layer>` namespace convention:
```
carbon_monitoring_service.src
carbon_monitoring_service.tests
```

## Build & Test

Locally, run everything:
```bash
pants package ::
pants test ::
```

Uses transitive dependencies to build a dependency chain of what's changed against the previous commit, then tests, packages and deploys:
```bash
pants test --changed-since=HEAD~1 --changed-dependents=transitive
pants package --changed-since=HEAD~1 --changed-dependents=transitive
pants experimental-deploy --changed-since=HEAD~1 --changed-dependents=transitive
```

## Architecture

**carbon monitoring service**: Express step function with 3 lambdas to process daily ingestion of carbon data
**carbon management service**: Lambda + Gateway to handle user interaction with managing data, permissions, owernership and management of which sites to monitor.

## Stack

Python 3.11 • PantsBuild • AWS • ICOS
