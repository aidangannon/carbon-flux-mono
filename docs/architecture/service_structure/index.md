# Service structure index

- A service is a deployable unit. Each service at repo root follows: `src/` (own pants module), `tests/` (own pants module, references `src`), `deploy/` (Terraform)
- Use [`carbon_monitoring_service`](../../../carbon_monitoring_service) as the archetype implementation for every file below
- Source follows ports-and-adapters, layered inside out: `core` → `application/ports` + `application/slices` → `bootstrapping` → `entry_points`, with `infrastructure` and `crosscutting` supporting from the side

## What are you adding?

| Task | Read |
|---|---|
| A new domain type or domain rule | [`core.md`](./core.md) |
| A new event/command/API shape | [`contracts.md`](./contracts.md) |
| A new dependency a slice needs (repo, client) | [`ports.md`](./ports.md) |
| A new use case | [`slices.md`](./slices.md) |
| Wiring a new adapter into a port | [`bootstrapping.md`](./bootstrapping.md) |
| A new Lambda / web endpoint | [`entry_points.md`](./entry_points.md) |
| A new concrete adapter (DB, HTTP client, etc.) | [`infrastructure.md`](./infrastructure.md) |
| Env-derived config or shared constants | [`crosscutting.md`](./crosscutting.md) |
| A new test for any of the above | [`tests_layout.md`](./tests_layout.md) |
| Deploy/Terraform changes | [`deploy_layout.md`](./deploy_layout.md) |

See also: [coding standards](../../coding_standards/index.md) for the *how/why* behind these layers.
