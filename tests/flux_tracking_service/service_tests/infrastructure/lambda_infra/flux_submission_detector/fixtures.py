from pytest import fixture

from src.flux_tracking_service.flux_submission_detector.bootstrap import bootstrap
from src.flux_tracking_service.flux_submission_detector.handler import inner_handle
from tests.common import create_container_with_bootstrap, create_handler_with_inner_handle
from tests.flux_tracking_service.service_tests.infrastructure.lambda_infra.flux_submission_detector.config import override_settings


@fixture(scope='session')
def flux_submission_detector_container(database):
    return create_container_with_bootstrap(bootstrap)

@fixture(scope='session')
def flux_submission_detector_settings(flux_submission_detector_container):
    return override_settings(flux_submission_detector_container)

@fixture(scope='session')
def flux_submission_detector_handler(flux_submission_detector_settings):
    return create_handler_with_inner_handle(flux_submission_detector_settings, inner_handle)