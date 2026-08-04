# Logging

- Every operation logs its start/completion at the entry point, scoped with structured context so every log line in that request carries the same traceable fields: see `logger.contextualize(**{logging_values.OPERATION: ...})` in [`entry_points/get_files_for_submission.py`](../../../carbon_monitoring_service/src/entry_points/get_files_for_submission.py)
- Operation names are constants in [`crosscutting/logging_values.py`](../../../carbon_monitoring_service/src/crosscutting/logging_values.py), not inline strings: one source of truth, greppable
- When logging an error or a notable event inside a slice or adapter, include the specific properties on the request that let you trace the failure back to its cause (site id, submission id, timestamps), not just a generic message. See the submission-id logging in [`infrastructure/icos.py`](../../../carbon_monitoring_service/src/infrastructure/icos.py).

## This is tested, not decoration

Service tests assert on logs directly, see [`coding_standards/tests/asserting_logs.md`](../tests/asserting_logs.md). What you log here is part of the tested contract.
