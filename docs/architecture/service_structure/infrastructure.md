# `infrastructure/` — adapters

- Concrete adapter implementations
- Each file implements one or more [port](./ports.md) `Protocol`s — structurally, no inheritance
- Imports from `core` and `crosscutting` only
- See [`src/infrastructure/`](../../../carbon_monitoring_service/src/infrastructure)

Reference implementations: [`infrastructure/dynamo.py`](../../../carbon_monitoring_service/src/infrastructure/dynamo.py) (DynamoDB, `lru_cache`'d table handle), [`infrastructure/icos.py`](../../../carbon_monitoring_service/src/infrastructure/icos.py) (HTTP client).

Coding standard for writing adapters: [`coding_standards/code/typing.md`](../../coding_standards/code/typing.md) (satisfying a `Protocol`), [`coding_standards/code/performance.md`](../../coding_standards/code/performance.md) (`__slots__`, caching the expensive client separately from the stateless adapter class), [`coding_standards/code/imports.md`](../../coding_standards/code/imports.md) (importing third-party SDKs at module level).
