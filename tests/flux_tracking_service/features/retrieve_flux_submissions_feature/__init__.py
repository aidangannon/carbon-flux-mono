from src.common.handlers import LambdaHandle
from tests import BaseBddContext


class RetrieveFluxSubmissionsContext(BaseBddContext):
    sut: LambdaHandle
    lambda_return: dict