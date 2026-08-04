# `application/ports.py`: port interfaces

- Port interfaces defined as `Protocol` classes
- This is what the application layer talks to: no concrete infra here, just the shapes the infrastructure must satisfy
- Each port is declared as a module-level variable with a type but no value (e.g. `flux_client: FluxClient`). [`bootstrapping.py`](./bootstrapping.md) assigns the real value at runtime
- See [`src/application/ports.py`](../../../carbon_monitoring_service/src/application/ports.py)

Adding a new port:
1. Define the `Protocol` in `ports.py`
2. Declare the module-level variable typed against it
3. Implement a concrete adapter in [`infrastructure/`](./infrastructure.md)
4. Wire it in [`bootstrapping.py`](./bootstrapping.md)

Why this shape (not constructor injection / a container): [`coding_standards/code/dependency_injection.md`](../../coding_standards/code/dependency_injection.md). Why `Protocol` over an ABC: [`coding_standards/code/typing.md`](../../coding_standards/code/typing.md).
