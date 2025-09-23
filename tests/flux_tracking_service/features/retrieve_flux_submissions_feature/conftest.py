from pytest import fixture

from tests.flux_tracking_service.features.retrieve_flux_submissions_feature import RetrieveFluxSubmissionsContext


@fixture
def retrieve_flux_submissions_feature(ingest_handler, ingest_container, database, api_mocks):
    ctx = RetrieveFluxSubmissionsContext()
    ctx.table = database
    ctx.sut = ingest_handler
    ctx.requests_mock = api_mocks
    ctx.container = ingest_container
    return ctx