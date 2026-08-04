# Test standards index

Two main types of tests: **service tests** and **unit tests**. Service tests are primary.

## What are you doing?

| Task | Read |
|---|---|
| Understanding service tests generally | [`service_tests.md`](./service_tests.md) |
| Adding a new feature folder (`feature.py` + `steps.py`) | [`feature_folder.md`](./feature_folder.md) |
| Wiring a fixture / session-scoped setup | [`fixtures.md`](./fixtures.md) |
| Adding a shared/reusable step | [`common_steps.md`](./common_steps.md) |
| Mocking an external API (HTTP, canned responses) | [`api_mocks.md`](./api_mocks.md) |
| Asserting a log line in a scenario | [`asserting_logs.md`](./asserting_logs.md) |
| Writing a plain `pytest` unit test | [`unit_tests.md`](./unit_tests.md) |

See [`get_files_for_submission_feature/`](../../../carbon_monitoring_service/tests/service_tests/features/get_files_for_submission_feature/) as the archetype implementation referenced throughout this section.
