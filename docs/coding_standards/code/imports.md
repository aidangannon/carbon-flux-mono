# Module-level imports

[← Code standards index](./index.md)

- Import the module, not the symbol: `from carbon_monitoring_service.src.infrastructure import icos`, then reference `icos.IcosFluxClient`, never `from ...infrastructure.icos import IcosFluxClient`
- See [`bootstrapping.py`](../../../carbon_monitoring_service/src/bootstrapping.py) as the exemplar
- Applies to [ports](./dependency_injection.md), [infrastructure adapters](../../architecture/service_structure/infrastructure.md), and third-party/external libraries: anything with behavior you might need to swap, mock, or monkeypatch in a test

## Why

Importing the module keeps the module as the unit of encapsulation. A test can monkeypatch `icos.requests` or reassign `ports.flux_client` without needing the code under test to accept an injected dependency: the seam is the module itself. It also makes it unambiguous, when reading a slice or adapter, exactly where a name came from (`dynamo.lazy_table()` vs. a bare `lazy_table()` that could be from anywhere).
