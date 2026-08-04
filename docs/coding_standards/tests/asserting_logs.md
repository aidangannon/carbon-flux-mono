# Asserting logs

- Every service test scenario should assert logs, not just the happy-path result
- Assert message, level, and scoped properties (e.g. operation name) that should be present on every log in that request
- The `scoped_log_vars` field on the [context](./feature_folder.md#context) carries the properties expected on all logs for the operation
- Use `should_have_log_LEVEL_MESSAGE` and `should_have_log_LEVEL_MESSAGE_EXTRAS` from [`common_steps/log_steps.py`](../../../carbon_monitoring_service/tests/service_tests/infrastructure/common_steps/log_steps.py)
- See the log assertions in [`get_files_for_submission_feature.py`](../../../carbon_monitoring_service/tests/service_tests/features/get_files_for_submission_feature/get_files_for_submission_feature.py): every scenario asserts at least one log

This is the test-side half of [`coding_standards/code/logging.md`](../code/logging.md): what you're required to log is defined there, this is how you prove it.
