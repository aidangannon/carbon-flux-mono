# Dependency injection via ports (IOC)

- `application/ports.py` declares each dependency as a module-level variable, typed against a `Protocol`, with no value assigned — e.g. `monitored_site_repository: MonitoredSiteRepository`. See [`application/ports.py`](../../../carbon_monitoring_service/src/application/ports.py).
- `bootstrapping.py` assigns concrete adapters from `infrastructure/` onto those module attributes, once, before any handler runs: `ports.monitored_site_repository = dynamo.DynamoMonitoredSiteRepository()`. See [`bootstrapping.py`](../../../carbon_monitoring_service/src/bootstrapping.py).
- Slices call `ports.flux_client.retrieve_files(...)` directly — they ask the `ports` module for what they need at the point of use, rather than having it handed to them via constructor injection.

## Why this shape, not a container

- This is closer to a **service locator** than classic constructor-injected IOC: a slice reaches into `ports` for what it needs rather than receiving it as an argument.
- The difference from a "God container" IOC setup is that there's no reflection, no decorators, no autowiring magic resolving an object graph for you — `bootstrapping.configure_adapters()` is a handful of plain assignment statements you can read top to bottom and know exactly what's wired to what.
- Importing `application.ports` in a slice is effectively "autowiring" in the sense that every port is already live on that module once `configure_adapters()` has run — but it's explicit: the call site says exactly which port it's using, and you can `grep` for every consumer of a given port.

## Adding a new port

1. Define the `Protocol` in `ports.py` — see [`typing.md`](./typing.md)
2. Declare the module-level variable typed against it
3. Implement a concrete adapter in [`infrastructure/`](../../architecture/service_structure/infrastructure.md)
4. Assign it in `bootstrapping.configure_adapters()`

Why classes/containers aren't used more heavily here (Lambda cold start): [`performance.md`](./performance.md).
