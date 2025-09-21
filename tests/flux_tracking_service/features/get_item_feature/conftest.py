import uuid
from unittest.mock import Mock

from _pytest.fixtures import fixture

from tests.flux_tracking_service.features.get_item_feature.get_item_feature_steps import GetItemContext


@fixture
def get_item_feature(ingest_handler, ingest_container, database):
    context = GetItemContext()
    context.container = ingest_container
    context.sut = ingest_handler
    context.table = database
    context.item_id = str(uuid.uuid4())
    context.scoped_vars = {"nested_prop": "this is nested"}
    return context