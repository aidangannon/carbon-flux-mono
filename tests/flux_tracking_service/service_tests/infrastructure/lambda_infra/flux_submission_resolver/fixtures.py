from pytest import fixture

from src.flux_tracking_service.flux_submission_resolver.bootstrap import bootstrap
from src.flux_tracking_service.flux_submission_resolver.handler import inner_handle
from tests.common import create_container_with_bootstrap, create_handler_with_inner_handle
from tests.flux_tracking_service.service_tests.infrastructure.lambda_infra.flux_submission_resolver.config import override_settings


@fixture(scope='session')
def flux_submission_resolver_container(database):
    return create_container_with_bootstrap(bootstrap)

@fixture(scope='session')
def flux_submission_resolver_settings(flux_submission_resolver_container):
    return override_settings(flux_submission_resolver_container)

@fixture(scope='session')
def flux_submission_resolver_handler(flux_submission_resolver_settings):
    return create_handler_with_inner_handle(flux_submission_resolver_settings, inner_handle)