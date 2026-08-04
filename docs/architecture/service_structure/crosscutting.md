# `crosscutting/`: shared concerns

[← Service structure index](./index.md)

- Shared concerns used across all layers
- [`config.py`](../../../carbon_monitoring_service/src/crosscutting/config.py): reads config from env vars via `lru_cache`'d functions. Env vars are set by Terraform at deploy time.
- [`logging_values.py`](../../../carbon_monitoring_service/src/crosscutting/logging_values.py): constants for structured log fields (operation names etc.), see [`coding_standards/code/logging.md`](../../coding_standards/code/logging.md)

Adding a new env-derived setting: add a field to the relevant `@dataclass(frozen=True, slots=True)` settings class in `config.py` and an `lru_cache`'d accessor function, following `lazy_dynamo_settings()` / `lazy_icos_settings()`.
