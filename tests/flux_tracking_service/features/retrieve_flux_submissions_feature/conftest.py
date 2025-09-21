from pytest import fixture

from tests.flux_tracking_service.features.retrieve_flux_submissions_feature import RetrieveFluxSubmissionsContext


@fixture
def retrieve_flux_submissions_feature(ingest_handler):
    ctx = RetrieveFluxSubmissionsContext()
    ctx.sut = ingest_handler
    return ctx