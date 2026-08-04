# Feature folder

Each feature is a folder under [`tests/service_tests/features/`](../../../carbon_monitoring_service/tests/service_tests/features/):
- `<feature_name>.py`: the index, imports steps and assembles them into scenarios (given/when/then chains)
- `steps.py`: context class, fixture, and step definitions unique to this feature

See [`get_files_for_submission_feature/`](../../../carbon_monitoring_service/tests/service_tests/features/get_files_for_submission_feature/) as the reference.

## `feature.py`

- Imports step functions from `steps.py` and [`infrastructure/common_steps/`](./common_steps.md)
- Each test function assembles a scenario by chaining steps: `.given()`, `.and_also()`, `.when()`, `.then()`, `.run_all_steps()`
- Should read like a spec: the scenario name and step names tell the full story
- See [`get_files_for_submission_feature.py`](../../../carbon_monitoring_service/tests/service_tests/features/get_files_for_submission_feature/get_files_for_submission_feature.py)

## `steps.py`

- Defines the `Context` class, the [fixture](./fixtures.md), and all step functions for this feature
- Steps are decorated with `@step`, which wraps the step's arguments and returns a callable the runner can invoke
- Step names use `UPPERCASE_WORDS` for the dynamic parts of the name (e.g. `lambda_should_throw_EXCEPTION`) this must match an argument in the step such as `exception: Exception` which would then be dynamically inserted into the step name for clearer test steps
- See [`get_files_for_submission_feature/steps.py`](../../../carbon_monitoring_service/tests/service_tests/features/get_files_for_submission_feature/steps.py)

## Context

- Each feature defines a `Context` dataclass inheriting from `BaseBddContext`
- `BaseBddContext` provides the runner; the `Context` adds feature-specific state
- Carries the system under test (`sut`), infrastructure handles (table, log capture, requests mock), and test data (IDs, URLs, etc.)
- The context is the single mutable object passed through every step in the scenario
- See [`GetFilesForSubmissionContext`](../../../carbon_monitoring_service/tests/service_tests/features/get_files_for_submission_feature/steps.py)
