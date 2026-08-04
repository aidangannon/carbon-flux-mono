# Performance: classes, caching, and Lambda cold starts

## Why not classes/containers for everything

- Classes are cheap to define but not free to instantiate repeatedly, and a full IOC container (reflection-based autowiring, object graphs resolved at startup) adds real overhead: bad news for Lambda, where cold start time is a cost you pay on every scale-out
- Lambda reuses warm execution environments between invocations. Anything held at module scope survives across warm invocations for free. So instead of a container caching a graph of services, we cache only the things that are genuinely expensive to create (network clients, table handles) as module-level, `lru_cache`'d functions:
  - [`infrastructure/dynamo.py`](../../../carbon_monitoring_service/src/infrastructure/dynamo.py) `lazy_table()`
  - [`crosscutting/config.py`](../../../carbon_monitoring_service/src/crosscutting/config.py) `lazy_dynamo_settings()` / `lazy_icos_settings()`
- Adapter classes themselves (`DynamoMonitoredSiteRepository`, `IcosFluxClient`) are cheap and stateless (no `__init__`, nothing to warm), so [`bootstrapping.configure_adapters()`](../../architecture/service_structure/bootstrapping.md) can freely construct fresh ones on every cold start. The expensive part (the boto3 client, the requests session) is memoized separately behind `lazy_table()`, so it's the same object across warm invocations regardless of how many times the adapter class gets constructed.
- Net effect: nothing is a "service" living in a container. Everything is either a stateless class constructed on demand, or a cached function-scoped resource.

## `__slots__`

- Regular classes: declare `__slots__` explicitly, even if empty, e.g. `__slots__ = ()` on stateless adapters like [`IcosFluxClient`](../../../carbon_monitoring_service/src/infrastructure/icos.py) and [`DynamoMonitoredSiteRepository`](../../../carbon_monitoring_service/src/infrastructure/dynamo.py)
- Dataclasses: `@dataclass(frozen=True, slots=True)`, see every model in [`core.py`](../../../carbon_monitoring_service/src/core.py)
- Why: without `__slots__` every instance carries a `__dict__`, which costs memory and slows attribute access. Given adapter classes get freely constructed on cold start, keeping them slotted and stateless keeps that cost near zero. Only opt out when an object genuinely needs dynamic attributes, that should be rare.
