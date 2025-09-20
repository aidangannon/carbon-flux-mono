import uuid
from unittest.mock import Mock

from _pytest.fixtures import fixture

from src.flux_tracking_service.ingest.services import AnotherDependency
from tests.flux_tracking_service.features.get_item_feature.get_item_feature_steps import TestScenarioContext


@fixture
def get_item_feature(handler, container, database):
    context = TestScenarioContext()
    container.register(AnotherDependency, instance=Mock())
    context.sut = handler
    context.table = database
    context.item_id = str(uuid.uuid4())
    return context