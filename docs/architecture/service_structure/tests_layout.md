# `tests/` layout

[← Service structure index](./index.md)

- All tests are service-level: they invoke entry point handlers end-to-end with real infra mocked at the boundary (moto for DynamoDB, `responses` for HTTP)
- No unit tests per layer
- Tests use the BDD runner from [`pyight_bdd`](../../../pyight_bdd)
- Each feature gets its own folder under [`tests/service_tests/features/`](../../../carbon_monitoring_service/tests/service_tests/features)
- Shared test infrastructure lives in [`tests/service_tests/infrastructure/`](../../../carbon_monitoring_service/tests/service_tests/infrastructure)
- Fixtures are set up in [`tests/service_tests/conftest.py`](../../../carbon_monitoring_service/tests/service_tests/conftest.py), scoped at `session` level where possible

Full breakdown (feature folder, fixtures, common_steps, api_mocks, asserting logs, unit tests): [`coding_standards/tests/index.md`](../../coding_standards/tests/index.md).
