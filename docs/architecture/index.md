# Architecture index

[← Index](../index.md)

| Doc | Covers |
|---|---|
| [Repo structure](./repo_structure.md) | Top-level repo layout: services vs. shared libraries, what belongs at root |
| [Build system](./build_system.md) | Pants, BUILD files, CI/CD, coding standard for defining new BUILD modules |
| [Service structure](./service_structure/index.md) | Layer-by-layer breakdown of a service. Start here if you're adding to an existing layer (`core`, `ports`, `slices`, `bootstrapping`, `entry_points`, `infrastructure`, `crosscutting`) or to `tests`/`deploy` |

`carbon_monitoring_service` is the reference implementation for everything below.
