# `entry_points/`: Lambda handlers / web endpoints

- Lambda handlers, one file per lambda
- Each file calls `bootstrapping.configure_adapters()` at module load to wire up ports, then defines a `handle(event, context)` function that calls the relevant slice and serialises the result to a dict
- Each entry point gets its own `python_aws_lambda_function` target in [`src/entry_points/BUILD`](../../../carbon_monitoring_service/src/entry_points/BUILD), which is what pants packages into a zippable Lambda artifact
- See [`src/entry_points/`](../../../carbon_monitoring_service/src/entry_points)

Adding a new endpoint:
1. Create `entry_points/<name>.py`
2. Call `bootstrapping.configure_adapters()` at module load
3. Wrap the handler body in `logging.logger.contextualize(**{logging_values.OPERATION: ...})`, see [`coding_standards/code/logging.md`](../../coding_standards/code/logging.md)
4. Call the relevant [slice](./slices.md), map its return value to a response dict
5. Add a `python_aws_lambda_function` target in `entry_points/BUILD`
6. Add a matching [service test](../../coding_standards/tests/service_tests.md)

Reference: [`entry_points/get_files_for_submission.py`](../../../carbon_monitoring_service/src/entry_points/get_files_for_submission.py).
