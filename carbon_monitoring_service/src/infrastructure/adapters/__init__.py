from carbon_monitoring_service.src.application import ports
from carbon_monitoring_service.src.infrastructure.adapters import dynamo
from carbon_monitoring_service.src.infrastructure.adapters import icos


dynamo_monitored_site_repository: ports.MonitoredSiteRepository = dynamo.DynamoMonitoredSiteRepository()
icos_flux_client: ports.FluxClient = icos.IcosFluxClient()
