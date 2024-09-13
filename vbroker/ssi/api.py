from ..interface_broker_api import IBrokerAPI


class SSIBrokerAPI(IBrokerAPI):
    def __init__(self, config):
        self.config = config

    def get_token(self):
        return "token"
