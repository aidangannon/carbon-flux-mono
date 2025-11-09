from punq import Container

from src.flux_tracking_service.config import DynamoSettings
from src.flux_tracking_service.crosscutting.config import IcosSettings
from tests.flux_tracking_service.service_tests.infrastructure.api_mocks import icos
from tests.flux_tracking_service.service_tests.infrastructure.config import DYNAMO_DB_TABLE, AWS_REGION


def override_settings(container: Container):
    override_icos_settings(container=container)
    return container

def override_icos_settings(container: Container):
    test_icos_settings = IcosSettings(
        data_url=icos.DATA_URL
    )
    test_dynamo_settings = DynamoSettings(
        table_name=DYNAMO_DB_TABLE,
        region=AWS_REGION
    )
    container.register(IcosSettings, instance=test_icos_settings)
    container.register(DynamoSettings, instance=test_dynamo_settings)