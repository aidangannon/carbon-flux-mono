# `bootstrapping.py`: wiring

- Wires concrete infrastructure adapters into the [`ports`](./ports.md) module at runtime
- Called once, at handler cold start (from the top of each [`entry_points/`](./entry_points.md) file)
- Plain assignment statements: no reflection, no autowiring, readable top to bottom
- See [`src/bootstrapping.py`](../../../carbon_monitoring_service/src/bootstrapping.py)

Adding a new adapter here: assign it onto its matching `ports.*` attribute. See [`coding_standards/code/dependency_injection.md`](../../coding_standards/code/dependency_injection.md) for the full philosophy and [`coding_standards/code/performance.md`](../../coding_standards/code/performance.md) for why this can construct fresh adapter instances on every cold start without a performance concern.
