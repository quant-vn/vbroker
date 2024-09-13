""" Interface for Broker API """
from abc import ABC, abstractmethod
from .config import Config


class IBrokerAPI(ABC):
    def __init__(self, config: Config):
        self.config: Config = config

    @abstractmethod
    def get_token(self) -> str:
        return NotImplemented
