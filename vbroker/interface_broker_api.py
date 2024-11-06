""" Interface for Broker API """
from typing import List
from abc import ABC, abstractmethod
from .config import Config
from .model import vBrokerOrder


class IBrokerAPI(ABC):
    def __init__(self, config: Config):
        self.config: Config = config
        self.otp: str = None

    @property
    def otp(self) -> str:
        return self._otp

    @otp.setter
    def otp(self, value: str):
        self._otp = value

    @abstractmethod
    def get_otp(self) -> str:
        return NotImplemented

    @abstractmethod
    def get_token(self) -> str:
        return NotImplemented

    @abstractmethod
    def get_max_buy_quantity(self, account_no: str, instrument: str, price: float) -> dict:
        return NotImplemented

    @abstractmethod
    def get_max_sell_quantity(self, account_no: str, instrument: str, price: float) -> dict:
        return NotImplemented

    @abstractmethod
    def get_ordebbook(self, account_no: str, from_date: str, to_date: str) -> List[vBrokerOrder]:
        return NotImplemented

    @abstractmethod
    def get_positions(self, account_no: str, is_equity: bool = True) -> dict:
        return NotImplemented

    @abstractmethod
    def get_balance(self, account_no: str, is_equity: bool = True) -> dict:
        return NotImplemented

    @abstractmethod
    def place_order(
        self, account_no: str, side: str, instrument: str,
        quantity: int, price: float | str, is_equity: bool = True
    ) -> dict:
        return NotImplemented

    @abstractmethod
    def modify_order(
        self, account_no: str, order_id: str,
        side: str, instrument: str, quantity: int, price: float | str, is_equity: bool = True
    ) -> dict:
        return NotImplemented

    @abstractmethod
    def cancel_order(
        self, account_no: str, order_id: str, instrument: str, side: str, is_equity: bool = True
    ) -> dict:
        return NotImplemented
