# Service structure

- A service is a deployable unit. Each service at repo root follows this layout:
  - `src/`: source code (its own pants module)
  - `tests/`: test suite (its own pants module, references src)
  - `deploy/`: Terraform
- See [`carbon_monitoring_service`](../../carbon_monitoring_service) as the archetype implementation

## src layout

- Source follows a ports-and-adapters pattern, layers from inside out:

### `core.py`
- Domain models: plain immutable dataclasses
- No imports from any other layer
- See [`src/core.py`](../../carbon_monitoring_service/src/core.py)

### `contracts.py`
- Contracts of the service, scoped to its domain: events, commands, API responses, API requests
- Defined as a separate build artifact in [`src/BUILD`](../../carbon_monitoring_service/src/BUILD) so consumers can depend on it independently without pulling in the whole service

### `application/ports.py`
- Port interfaces defined as `Protocol` classes
- This is what the application layer talks to: no concrete infra here, just the shapes the infrastructure must satisfy
- See [`src/application/ports.py`](../../carbon_monitoring_service/src/application/ports.py)

### `application/slices/`
- One file per use case
- Each slice calls ports to do its work, returns domain types
- No infra imports, no Lambda-specific concerns
- See [`src/application/slices/`](../../carbon_monitoring_service/src/application/slices)

### `bootstrapping.py`
- Wires concrete infrastructure adapters into the ports module at runtime
- Called once at handler startup
- See [`src/bootstrapping.py`](../../carbon_monitoring_service/src/bootstrapping.py)

### `entry_points/`
- Lambda handlers, one file per lambda
- Each file calls `bootstrapping.configure_adapters()` at module load to wire up ports, then defines a `handle(event, context)` function that calls the relevant slice and serialises the result to a dict
- Each entry point gets its own `python_aws_lambda_function` target in [`src/entry_points/BUILD`](../../carbon_monitoring_service/src/entry_points/BUILD), which is what pants packages into a zippable Lambda artifact
- See [`src/entry_points/`](../../carbon_monitoring_service/src/entry_points)

### `infrastructure/`
- Concrete adapter implementations
- Each file implements one or more port Protocols
- Imports from `core` and `crosscutting` only
- See [`src/infrastructure/`](../../carbon_monitoring_service/src/infrastructure)

### `crosscutting/`
- Shared concerns used across all layers
- [`config.py`](../../carbon_monitoring_service/src/crosscutting/config.py): reads config from env vars via `lru_cache`'d functions. Env vars are set by Terraform at deploy time.
- [`logging_values.py`](../../carbon_monitoring_service/src/crosscutting/logging_values.py): constants for structured log fields (operation names etc.)

## tests layout

- All tests are service-level: they invoke entry point handlers end-to-end with real infra mocked at the boundary (moto for DynamoDB, `responses` for HTTP)
- No unit tests per layer
- Tests use the BDD runner from [`pyight_bdd`](../../pyight_bdd)
- Each feature gets its own folder under [`tests/service_tests/features/`](../../carbon_monitoring_service/tests/service_tests/features):
  - `<feature_name>.py`: test cases (given/when/then chains)
  - `steps.py`: step implementations + context dataclass
- Shared test infrastructure lives in [`tests/service_tests/infrastructure/`](../../carbon_monitoring_service/tests/service_tests/infrastructure):
  - `api_mocks/`: canned HTTP responses for external APIs
  - `common_steps/`: reusable step definitions shared across features
- Fixtures (database, env vars, logging capture, HTTP mocks) are set up in [`tests/service_tests/conftest.py`](../../carbon_monitoring_service/tests/service_tests/conftest.py) and scoped at `session` level where possible

## deploy layout

- Terraform for the service lives in [`deploy/`](../../carbon_monitoring_service/deploy)
- Deployed via `pants experimental-deploy` in CI (see [`build_system.md`](./build_system.md)), which runs `terraform apply -auto-approve` only on push to trunk and only when `pants package` produced artifacts
