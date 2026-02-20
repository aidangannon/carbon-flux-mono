from carbon_monitoring_service.src.infrastructure import adapters
from carbon_monitoring_service.src.application import ports


__all__ = ["configure_adapters"]

def configure_adapters():
    ports.monitored_site_repository = adapters.dynamo_monitored_site_repository
    ports.flux_client = adapters.icos_flux_client
