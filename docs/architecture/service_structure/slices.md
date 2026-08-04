# `application/slices/` — use cases

- One file per use case
- Each slice calls ports to do its work, coordinates with `core`, and returns domain types
- No infra imports, no Lambda-specific concerns — a slice doesn't know it's running in a Lambda
- See [`src/application/slices/`](../../../carbon_monitoring_service/src/application/slices)

Coding standard for writing slices: [`coding_standards/code/layering.md`](../../coding_standards/code/layering.md), [`coding_standards/code/dependency_injection.md`](../../coding_standards/code/dependency_injection.md) (calling `ports`).
