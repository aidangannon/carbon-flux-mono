# Coding standards

See [`service_structure.md`](../architecture/service_structure.md) for the full layer layout. This doc covers the standards behind those layers: where logic goes, how dependencies get wired, and how to write code within each layer.

## Where logic goes

- **Domain logic** → `core.py`: plain, frozen, immutable dataclasses and free functions that operate on them. No imports from `application`, `infrastructure`, or `crosscutting`. See [`src/core.py`](../../carbon_monitoring_service/src/core.py).
- **Application logic** → `application/slices/*.py`: one file per use case. A slice glues calls to ports together, coordinates calls into `core`, and returns domain types. It has no infra imports and no Lambda-specific concerns — it doesn't know it's running in a Lambda. See [`get_files_for_submission.py`](../../carbon_monitoring_service/src/application/slices/get_files_for_submission.py).
- If you're deciding between the two: does this logic need I/O (a port)? → slice. Is it a pure transformation/rule over domain data? → core.

## Dependency injection via ports

- `application/ports.py` declares each dependency as a module-level variable, typed against a `Protocol`, with no value assigned — e.g. `monitored_site_repository: MonitoredSiteRepository`. See [`application/ports.py`](../../carbon_monitoring_service/src/application/ports.py).
- `bootstrapping.py` assigns concrete adapters from `infrastructure/` onto those module attributes, once, before any handler runs: `ports.monitored_site_repository = dynamo.DynamoMonitoredSiteRepository()`. See [`bootstrapping.py`](../../carbon_monitoring_service/src/bootstrapping.py).
- Slices call `ports.flux_client.retrieve_files(...)` directly — they ask the `ports` module for what they need at the point of use, rather than having it handed to them via constructor injection.
- This is closer to a **service locator** than classic constructor-injected IOC: a slice reaches into `ports` for what it needs rather than receiving it as an argument. The difference from a "God container" IOC setup is that there's no reflection, no decorators, no autowiring magic resolving an object graph for you — `bootstrapping.configure_adapters()` is a handful of plain assignment statements you can read top to bottom and know exactly what's wired to what.
- Importing `application.ports` in a slice is effectively "autowiring" in the sense that every port is already live on that module once `configure_adapters()` has run — but it's explicit: the call site says exactly which port it's using, and you can `grep` for every consumer of a given port.

## Why not classes/containers for everything

- Classes are cheap to define but not free to instantiate repeatedly, and a full IOC container (reflection-based autowiring, object graphs resolved at startup) adds real overhead — bad news for Lambda, where cold start time is a cost you pay on every scale-out.
- Lambda reuses warm execution environments between invocations. Anything held at module scope survives across warm invocations for free. So instead of a container caching a graph of services, we cache only the things that are genuinely expensive to create — network clients, table handles — as module-level, `lru_cache`'d functions:
  - [`infrastructure/dynamo.py`](../../carbon_monitoring_service/src/infrastructure/dynamo.py) `lazy_table()`
  - [`crosscutting/config.py`](../../carbon_monitoring_service/src/crosscutting/config.py) `lazy_dynamo_settings()` / `lazy_icos_settings()`
- Adapter classes themselves (`DynamoMonitoredSiteRepository`, `IcosFluxClient`) are cheap and stateless — no `__init__`, nothing to warm — so `bootstrapping.configure_adapters()` can freely construct fresh ones on every cold start. The expensive part (the boto3 client, the requests session) is memoized separately behind `lazy_table()`, so it's the same object across warm invocations regardless of how many times the adapter class gets constructed.
- Net effect: nothing is a "service" living in a container. Everything is either a stateless class constructed on demand, or a cached function-scoped resource. `bootstrapping.py` is the entire wiring story, run once, with no magic.

## Module-level imports

- Import the module, not the symbol: `from carbon_monitoring_service.src.infrastructure import icos`, then reference `icos.IcosFluxClient` — never `from ...infrastructure.icos import IcosFluxClient`. See [`bootstrapping.py`](../../carbon_monitoring_service/src/bootstrapping.py) as the exemplar.
- Applies to ports, infrastructure adapters, and third-party/external libraries — anything with behavior you might need to swap, mock, or monkeypatch in a test.
- Why: importing the module keeps the module as the unit of encapsulation. A test can monkeypatch `icos.requests` or reassign `ports.flux_client` without needing the code under test to accept an injected dependency — the seam is the module itself. It also makes it unambiguous, when reading a slice or adapter, exactly where a name came from (`dynamo.lazy_table()` vs. a bare `lazy_table()` that could be from anywhere).

## Protocols, not base classes

- `application/ports.py` types each port as a `@runtime_checkable` `Protocol` (see [`MonitoredSiteRepository`, `FluxClient`](../../carbon_monitoring_service/src/application/ports.py)).
- Adapters in `infrastructure/` don't inherit from these Protocols — `DynamoMonitoredSiteRepository` and `IcosFluxClient` just implement the matching methods. Structural typing means anything with the right shape satisfies the port; no base class coupling infra to application.
- Prefer this over ABCs for any interface an adapter or test double needs to satisfy.

## `__slots__`

- Regular classes: declare `__slots__` explicitly, even if empty — `__slots__ = ()` on stateless adapters like [`IcosFluxClient`](../../carbon_monitoring_service/src/infrastructure/icos.py) and [`DynamoMonitoredSiteRepository`](../../carbon_monitoring_service/src/infrastructure/dynamo.py).
- Dataclasses: `@dataclass(frozen=True, slots=True)` — see every model in [`core.py`](../../carbon_monitoring_service/src/core.py).
- Why: without `__slots__` every instance carries a `__dict__`, which costs memory and slows attribute access. Given adapter classes get freely constructed on cold start (see above), keeping them slotted and stateless keeps that cost near zero. Only opt out when an object genuinely needs dynamic attributes — that should be rare.

## Logging

- Every operation logs its start/completion at the entry point, scoped with structured context so every log line in that request carries the same traceable fields — see `logger.contextualize(**{logging_values.OPERATION: ...})` in [`entry_points/get_files_for_submission.py`](../../carbon_monitoring_service/src/entry_points/get_files_for_submission.py).
- Operation names are constants in [`crosscutting/logging_values.py`](../../carbon_monitoring_service/src/crosscutting/logging_values.py), not inline strings — one source of truth, greppable.
- When logging an error or a notable event inside a slice or adapter, include the specific properties on the request that let you trace the failure back to its cause (site id, submission id, timestamps) — not just a generic message. See the submission-id logging in [`infrastructure/icos.py`](../../carbon_monitoring_service/src/infrastructure/icos.py).
- This isn't optional decoration: service tests assert on logs directly (see [`tests.md` § Asserting logs](./tests.md#asserting-logs)), so what you log here is part of the tested contract, not an afterthought.
