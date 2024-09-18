""" Interface for Broker API """
from abc import ABC, abstractmethod
from .config import Config


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
    def get_order_history(self) -> dict:
        return NotImplemented

    @abstractmethod
    def get_orderbook(self) -> dict:
        return NotImplemented

    @abstractmethod
    def get_max_buy_quantity(self, account_no: str, instrument: str, price: float) -> dict:
        return NotImplemented

    @abstractmethod
    def get_max_sell_quantity(self, account_no: str, instrument: str, price: float) -> dict:
        return NotImplemented

    # EQUITY
    @abstractmethod
    def get_equity_positions(self, account_no: str) -> dict:
        return NotImplemented

    @abstractmethod
    def get_equity_account_balance(self, account_no: str) -> dict:
        return NotImplemented

    @abstractmethod
    def place_equity_order(
        self, account_no: str, side: str, instrument: str, quantity: int, price: float
    ) -> dict:
        return NotImplemented

    # DERIVATIVES
    @abstractmethod
    def get_derivative_positions(self, account_no: str) -> dict:
        return NotImplemented

    @abstractmethod
    def get_derivative_account_balance(self, account_no: str) -> dict:
        return NotImplemented

    @abstractmethod
    def place_derivative_order(
        self, account_no: str, side: str, instrument: str, quantity: int, price: float
    ) -> dict:
        return NotImplemented
