from carbon_monitoring_service.src.infrastructure.adapters import icos_flux_client
from carbon_monitoring_service.src.infrastructure.adapters import dynamo_monitored_site_repository
from carbon_monitoring_service.src.application import ports


__all__ = ["configure_adapters"]

def configure_adapters():
    ports.monitored_site_repository = dynamo_monitored_site_repository
    ports.flux_client = icos_flux_client
