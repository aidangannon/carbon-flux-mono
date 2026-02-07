import carbon_monitoring_service.src.infrastructure.adapters.icos_flux_client as icos_flux_client
import carbon_monitoring_service.src.infrastructure.adapters.dynamo_monitored_site_repository as dynamo_monitored_site_repository
import carbon_monitoring_service.src.application.ports as ports


__all__ = ["configure_adapters"]

def configure_adapters():
    ports.monitored_site_repository = dynamo_monitored_site_repository
    ports.flux_client = icos_flux_client
