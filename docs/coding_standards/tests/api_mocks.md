# `api_mocks` (and other infra helpers)

- [`tests/service_tests/infrastructure/api_mocks/`](../../../carbon_monitoring_service/tests/service_tests/infrastructure/api_mocks/) does the heavy lifting: configuring `responses` mocks, building response payloads, etc.
- [Common steps](./common_steps.md) delegate to these helpers — they don't configure mocks themselves
- See [`infrastructure/api_mocks/icos.py`](../../../carbon_monitoring_service/tests/service_tests/infrastructure/api_mocks/icos.py)
