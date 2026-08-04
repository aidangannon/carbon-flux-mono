# Fixtures

[← Test standards index](./index.md)

- Defined in `steps.py`, named after the feature
- Instantiates the [`Context`](./feature_folder.md#context), wires in session-scoped fixtures (`database`, `logging`, `api_mocks`), and seeds test data via `auto_fixture`
- Imported in [`tests/service_tests/features/conftest.py`](../../../carbon_monitoring_service/tests/service_tests/features/conftest.py) so pytest auto-discovers it at runtime
- Session-scoped fixtures (database, env vars, logging capture, HTTP mocks) live in [`tests/service_tests/conftest.py`](../../../carbon_monitoring_service/tests/service_tests/conftest.py), scoped at `session` level where possible; don't re-create expensive fixtures per-test
