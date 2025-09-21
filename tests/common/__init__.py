from punq import Container

from src.common.handlers import IocHandle, InnerLambdaHandle
from tests import add_test_logging


def create_handler_with_inner_handle(container: Container, inner_handle_func: InnerLambdaHandle):
    return lambda event, context: inner_handle_func(container, event, context)

def create_container_with_bootstrap(bootstrap_func: IocHandle):
    container = Container()
    bootstrap_func(container)
    add_test_logging(container=container)
    return container