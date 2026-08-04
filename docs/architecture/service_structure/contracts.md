# `contracts.py`: service contracts

- Contracts of the service, scoped to its domain: events, commands, API responses, API requests
- Defined as a separate build artifact in [`src/BUILD`](../../../carbon_monitoring_service/src/BUILD) so consumers can depend on it independently without pulling in the whole service
- See [`src/contracts.py`](../../../carbon_monitoring_service/src/contracts.py)
