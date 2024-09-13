""" This module defines the interface for a broker HUB. """
from abc import ABC, abstractmethod


class IBrokerHUB(ABC):
    def __init__(self, api):
        self.api = api
        self.__token: str = None

    @property
    def token(self) -> str:
        """
        Returns the token used for authentication.
        Returns:
            str: The authentication token.
        """
        return self.__token

    @token.setter
    def token(self, value: str):
        self.__token = value

    @abstractmethod
    async def listen(self, args, on_message):
        """
        Listens for incoming messages from the broker.
        Args:
            args: The arguments for the listen method.
            on_message: The callback function to be executed when a message is received.
        Returns:
            NotImplemented
        """
        return NotImplemented
