# Protocols, not base classes

- `application/ports.py` types each port as a `@runtime_checkable` `Protocol` — see [`MonitoredSiteRepository`, `FluxClient`](../../../carbon_monitoring_service/src/application/ports.py)
- Adapters in `infrastructure/` don't inherit from these Protocols — `DynamoMonitoredSiteRepository` and `IcosFluxClient` just implement the matching methods. Structural typing means anything with the right shape satisfies the port; no base class coupling infra to application.
- Prefer this over ABCs for any interface an adapter or test double needs to satisfy

See [`dependency_injection.md`](./dependency_injection.md) for how these get wired at runtime, and [`../../architecture/service_structure/ports.md`](../../architecture/service_structure/ports.md) for where they live on disk.
