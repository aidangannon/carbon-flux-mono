from punq import Container

from src.flux_tracking_service.ingest.config import IcosSettings
from tests.flux_tracking_service.infrastructure.api_mocks import icos


def override_settings(container: Container):
    override_icos_settings(container=container)
    return container

def override_icos_settings(container: Container):
    test_icos_settings = IcosSettings(
        data_url=icos.DATA_URL,
        meta_url=icos.META_URL
    )
    container.register(IcosSettings, instance=test_icos_settings)