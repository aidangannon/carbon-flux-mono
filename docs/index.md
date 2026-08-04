# Index

- A tree of markdown files: this index points to sections, sections point to more docs, docs point to files and line numbers in the code
- Every file in this tree is small and single-topic: find the one you need from the tables below, you shouldn't need to read siblings

## By section

| Section | Covers |
|---|---|
| [Architecture](./architecture/index.md) | Repo layout, build system, service layer-by-layer (where does a new port/slice/endpoint go) |
| [Coding standards](./coding_standards/index.md) | Rules for writing code within each layer, and for writing tests |
| [Reading the code](./reading_the_code/index.md) | (empty, TODO) |
| [Running the app](./running_the_app/index.md) | (empty, TODO) |

## Common tasks, straight to the doc

| I want to... | Read |
|---|---|
| Add a new domain type/rule | [`architecture/service_structure/core.md`](./architecture/service_structure/core.md) |
| Add a new use case | [`architecture/service_structure/slices.md`](./architecture/service_structure/slices.md) |
| Add/wire a new port or adapter (IOC) | [`coding_standards/code/dependency_injection.md`](./coding_standards/code/dependency_injection.md) |
| Add a new Lambda / web endpoint | [`architecture/service_structure/entry_points.md`](./architecture/service_structure/entry_points.md) |
| Add a service test | [`coding_standards/tests/service_tests.md`](./coding_standards/tests/service_tests.md) |
| Add a fixture | [`coding_standards/tests/fixtures.md`](./coding_standards/tests/fixtures.md) |
| Add a shared test step | [`coding_standards/tests/common_steps.md`](./coding_standards/tests/common_steps.md) |
| Add a log line | [`coding_standards/code/logging.md`](./coding_standards/code/logging.md) |
| Add a new BUILD target | [`architecture/build_system.md`](./architecture/build_system.md) |
