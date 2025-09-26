from punq import Container

from src.flux_tracking_service.config import DynamoSettings
from src.flux_tracking_service.ingest.config import IcosSettings
from tests.flux_tracking_service.service_tests.infrastructure.api_mocks import icos

DYNAMO_DB_TABLE = "testing"
AWS_REGION = "eu-west-2"

def override_settings(container: Container):
    override_icos_settings(container=container)
    return container

def override_icos_settings(container: Container):
    test_icos_settings = IcosSettings(
        data_url=icos.DATA_URL,
        meta_url=icos.META_URL_NON_HTTPS
    )
    test_dynamo_settings = DynamoSettings(
        table_name=DYNAMO_DB_TABLE,
        region=AWS_REGION
    )
    container.register(IcosSettings, instance=test_icos_settings)
    container.register(DynamoSettings, instance=test_dynamo_settings)