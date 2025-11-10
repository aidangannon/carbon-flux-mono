from responses import RequestsMock

from tests import BaseBddContext


class RequestContext(BaseBddContext):
    api_mocks: RequestsMock