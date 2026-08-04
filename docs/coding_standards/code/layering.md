# Layering: where does logic go?

- **Domain logic** → `core.py`: plain, frozen, immutable dataclasses and free functions that operate on them. No imports from `application`, `infrastructure`, or `crosscutting`. See [`src/core.py`](../../../carbon_monitoring_service/src/core.py) and [`architecture/service_structure/core.md`](../../architecture/service_structure/core.md).
- **Application logic** → `application/slices/*.py`: one file per use case. A slice glues calls to [ports](./dependency_injection.md) together, coordinates calls into `core`, and returns domain types. No infra imports, no Lambda-specific concerns. See [`get_files_for_submission.py`](../../../carbon_monitoring_service/src/application/slices/get_files_for_submission.py) and [`architecture/service_structure/slices.md`](../../architecture/service_structure/slices.md).

## Deciding

- Does this logic need I/O (a port)? → slice
- Is it a pure transformation/rule over domain data? → core
- Does it talk to boto3/requests/an SDK directly? → [`infrastructure/`](../../architecture/service_structure/infrastructure.md), never `core` or a slice
