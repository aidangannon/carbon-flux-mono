# `core.py` — domain layer

- Domain models: plain immutable dataclasses
- No imports from any other layer — `core` depends on nothing in `application`, `infrastructure`, or `crosscutting`
- Free functions that operate on domain types (pure transformations, rules) also belong here
- See [`src/core.py`](../../../carbon_monitoring_service/src/core.py)

Coding standard for writing domain code: [`coding_standards/code/layering.md`](../../coding_standards/code/layering.md), [`coding_standards/code/performance.md`](../../coding_standards/code/performance.md) (`slots=True`).
