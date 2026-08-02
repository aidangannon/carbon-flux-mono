# Testing standards

Two main types of tests: **service tests** and **unit tests**. Service tests are primary.

## Service tests

- The living document of what the code functionally does
- End-to-end: invoke entry point handlers directly with infrastructure mocked at the boundary (moto for DynamoDB, `responses` for HTTP)
- All cases should be captured here, and all run in parallel
- See [`carbon_monitoring_service/tests/service_tests/`](../../carbon_monitoring_service/tests/service_tests/) as the archetype implementation

### Feature folder

Each feature is a folder under [`tests/service_tests/features/`](../../carbon_monitoring_service/tests/service_tests/features/):
- `<feature_name>.py` — the index: imports steps and assembles them into scenarios (given/when/then chains)
- `steps.py` — context class, fixture, and step definitions unique to this feature

See [`get_files_for_submission_feature/`](../../carbon_monitoring_service/tests/service_tests/features/get_files_for_submission_feature/) as the reference.

### feature.py

- Imports step functions from `steps.py` and `infrastructure/common_steps/`
- Each test function assembles a scenario by chaining steps: `.given()`, `.and_also()`, `.when()`, `.then()`, `.run_all_steps()`
- Should read like a spec — the scenario name and step names tell the full story
- See [`get_files_for_submission_feature.py`](../../carbon_monitoring_service/tests/service_tests/features/get_files_for_submission_feature/get_files_for_submission_feature.py)

### steps.py

- Defines the `Context` class, the fixture, and all step functions for this feature
- Steps are decorated with `@step`, which wraps the step's arguments and returns a callable the runner can invoke
- Step names use `UPPERCASE_WORDS` for the dynamic parts of the name (e.g. `lambda_should_throw_EXCEPTION`) this must match an argument in the step such as `exception: Exception` which would then be dynamically inserted into the step name for clearer test steps
- See [`get_files_for_submission_feature/steps.py`](../../carbon_monitoring_service/tests/service_tests/features/get_files_for_submission_feature/steps.py)

### Context

- Each feature defines a `Context` dataclass inheriting from `BaseBddContext`
- `BaseBddContext` provides the runner; the `Context` adds feature-specific state
- Carries the system under test (`sut`), infrastructure handles (table, log capture, requests mock), and test data (IDs, URLs, etc.)
- The context is the single mutable object passed through every step in the scenario
- See [`GetFilesForSubmissionContext`](../../carbon_monitoring_service/tests/service_tests/features/get_files_for_submission_feature/steps.py)

### Fixture

- Defined in `steps.py`, named after the feature
- Instantiates the context, wires in session-scoped fixtures (`database`, `logging`, `api_mocks`), and seeds test data via `auto_fixture`
- Imported in [`tests/service_tests/features/conftest.py`](../../carbon_monitoring_service/tests/service_tests/features/conftest.py) so pytest auto-discovers it at runtime

### common_steps

- [`tests/service_tests/infrastructure/common_steps/`](../../carbon_monitoring_service/tests/service_tests/infrastructure/common_steps/) defines steps shared across features
- Must not be business-specific or entity-specific — only generic infrastructure coordination: setting up mocks, asserting HTTP status codes, asserting logs
- The common step coordinates; the underlying mock/infra helper does the actual work
- See [`common_steps/icos_steps.py`](../../carbon_monitoring_service/tests/service_tests/infrastructure/common_steps/icos_steps.py) and [`common_steps/log_steps.py`](../../carbon_monitoring_service/tests/service_tests/infrastructure/common_steps/log_steps.py)

### api_mocks (and other infra helpers)

- [`tests/service_tests/infrastructure/api_mocks/`](../../carbon_monitoring_service/tests/service_tests/infrastructure/api_mocks/) does the heavy lifting: configuring `responses` mocks, building response payloads, etc.
- Common steps delegate to these helpers — they don't configure mocks themselves
- See [`infrastructure/api_mocks/icos.py`](../../carbon_monitoring_service/tests/service_tests/infrastructure/api_mocks/icos.py)

### Asserting logs

- Every service test scenario should assert logs — not just the happy-path result
- Assert message, level, and scoped properties (e.g. operation name) that should be present on every log in that request
- The `scoped_log_vars` field on the context carries the properties expected on all logs for the operation
- Use `should_have_log_LEVEL_MESSAGE` and `should_have_log_LEVEL_MESSAGE_EXTRAS` from [`common_steps/log_steps.py`](../../carbon_monitoring_service/tests/service_tests/infrastructure/common_steps/log_steps.py)
- See the log assertions in [`get_files_for_submission_feature.py`](../../carbon_monitoring_service/tests/service_tests/features/get_files_for_submission_feature/get_files_for_submission_feature.py) — every scenario asserts at least one log

## Unit tests

- Only for mapping/transformation logic, or complex algorithms that need edge-case coverage
- Use `pytest` directly, no BDD
- Don't write unit tests for things already covered end-to-end by service tests
