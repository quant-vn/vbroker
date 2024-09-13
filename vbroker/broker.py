""" Broker module for broker API and HUB. """
from .config import Config

from .enum_broker import EnumBroker
from .interface_broker_api import IBrokerAPI
from .interface_broker_hub import IBrokerHUB

from .ssi import SSIBrokerAPI, SSIBrokerHUB


class Broker:
    def __init__(self, broker: EnumBroker, config: Config) -> None:
        if broker == EnumBroker.SSI.value:
            self.__api: IBrokerAPI = SSIBrokerAPI(config)
            self.__hub: IBrokerHUB = SSIBrokerHUB(self.__api)

    @property
    def api(self) -> IBrokerAPI:
        return self.__api

    @property
    def hub(self) -> IBrokerHUB:
        return self.__hub
