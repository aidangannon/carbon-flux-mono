# `common_steps`

- [`tests/service_tests/infrastructure/common_steps/`](../../../carbon_monitoring_service/tests/service_tests/infrastructure/common_steps/) defines steps shared across features
- Must not be business-specific or entity-specific, only generic infrastructure coordination: setting up mocks, asserting HTTP status codes, asserting logs
- The common step coordinates; the underlying mock/infra helper (see [`api_mocks.md`](./api_mocks.md)) does the actual work
- See [`common_steps/icos_steps.py`](../../../carbon_monitoring_service/tests/service_tests/infrastructure/common_steps/icos_steps.py) and [`common_steps/log_steps.py`](../../../carbon_monitoring_service/tests/service_tests/infrastructure/common_steps/log_steps.py)

Adding a new common step: put it here only if it's reusable across features. If it's specific to one feature's business logic, it belongs in that feature's [`steps.py`](./feature_folder.md#stepspy) instead.
