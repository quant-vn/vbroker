from ..interface_broker_hub import IBrokerHUB


class SSIBrokerHUB(IBrokerHUB):
    def __init__(self, api):
        super().__init__(api)

    async def listen(self, args, on_message):
        return NotImplemented
