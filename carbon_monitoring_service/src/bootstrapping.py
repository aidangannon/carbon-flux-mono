from carbon_monitoring_service.src.infrastructure import icos
from carbon_monitoring_service.src.infrastructure import dynamo
from carbon_monitoring_service.src.application import ports


__all__ = ["configure_adapters"]


def configure_adapters():
    ports.monitored_site_repository = dynamo.DynamoMonitoredSiteRepository()
    ports.flux_client = icos.IcosFluxClient()
