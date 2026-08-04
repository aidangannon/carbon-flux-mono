# Service tests

[← Test standards index](./index.md)

- The living document of what the code functionally does
- End-to-end: invoke entry point handlers directly with infrastructure mocked at the boundary (moto for DynamoDB, `responses` for HTTP)
- All cases should be captured here, and all run in parallel
- See [`carbon_monitoring_service/tests/service_tests/`](../../../carbon_monitoring_service/tests/service_tests/) as the archetype implementation

## Anatomy of a scenario

1. A [feature folder](./feature_folder.md) with `<feature_name>.py` (the scenarios) and `steps.py` (context + step defs)
2. A [fixture](./fixtures.md) that instantiates the context and wires in shared infra
3. [Common steps](./common_steps.md) for generic infra coordination, backed by [api_mocks](./api_mocks.md) for the actual mock setup
4. [Log assertions](./asserting_logs.md) on every scenario, not just the happy-path result
