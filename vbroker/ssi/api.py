import json
import os.path
from datetime import datetime
from nanoid import generate

from .constant import (
    API_URL,
    ENDPOINT_OTP,
    ENDPOINT_AUTH,

    ENDPOINT_EQUITY_NEW_ORDER,
    ENDPOINT_EQUITY_MODIFY_ORDER,
    ENDPOINT_EQUITY_CANCEL_ORDER,
    ENDPOINT_EQUITY_POSITION,
    ENDPOINT_EQUITY_ACCOUNT_BALANCE,

    ENDPOINT_DERIVATIVE_NEW_ORDER,
    ENDPOINT_DERIVATIVE_MODIFY_ORDER,
    ENDPOINT_DERIVATIVE_CANCEL_ORDER,
    ENDPOINT_DERIVATIVE_POSITION,
    ENDPOINT_DERIVATIVE_ACCOUNT_BALANCE,

    ENDPOINT_ORDER_HISTORY,
    ENDPOINT_ORDERBOOK,
    ENDPOINT_MAX_BUY_QUANTITY,
    ENDPOINT_MAX_SELL_QUANTITY
)
from .model import (
    OrderInfo,
    SSIPlaceOrderRequestModel,
    SSIModifyOrderRequestModel,
    SSICancelOrderRequestModel
)

from ..interface_broker_api import IBrokerAPI
from ..utils import jwt_handler, request_handler, sign, split_date_range


class SSIBrokerAPI(IBrokerAPI):
    def __init__(self, config):
        super().__init__(config)
        self.url_auth: str = "/".join([API_URL, ENDPOINT_AUTH])
        self.url_otp: str = "/".join([API_URL, ENDPOINT_OTP])
        self.url_equity_new_order: str = "/".join([API_URL, ENDPOINT_EQUITY_NEW_ORDER])
        self.url_equity_modify_order: str = "/".join([API_URL, ENDPOINT_EQUITY_MODIFY_ORDER])
        self.url_equity_cancel_order: str = "/".join([API_URL, ENDPOINT_EQUITY_CANCEL_ORDER])
        self.url_equity_position: str = "/".join([API_URL, ENDPOINT_EQUITY_POSITION])
        self.url_equity_account_balance: str = "/".join([API_URL, ENDPOINT_EQUITY_ACCOUNT_BALANCE])
        self.url_derivative_new_order: str = "/".join([API_URL, ENDPOINT_DERIVATIVE_NEW_ORDER])
        self.url_derivative_modify_order: str = "/".join(
            [API_URL, ENDPOINT_DERIVATIVE_MODIFY_ORDER]
        )
        self.url_derivative_cancel_order: str = "/".join(
            [API_URL, ENDPOINT_DERIVATIVE_CANCEL_ORDER]
        )
        self.url_derivative_position: str = "/".join([API_URL, ENDPOINT_DERIVATIVE_POSITION])
        self.url_derivative_account_balance: str = "/".join(
            [API_URL, ENDPOINT_DERIVATIVE_ACCOUNT_BALANCE]
        )
        self.url_order_history: str = "/".join([API_URL, ENDPOINT_ORDER_HISTORY])
        self.url_orderbook: str = "/".join([API_URL, ENDPOINT_ORDERBOOK])
        self.url_max_buy_quantity: str = "/".join([API_URL, ENDPOINT_MAX_BUY_QUANTITY])
        self.url_max_sell_quantity: str = "/".join([API_URL, ENDPOINT_MAX_SELL_QUANTITY])
        self.__equity_market_id: str = "VN"
        self.__derivative_market_id: str = "VNFE"
        self.__session_file: str = "vbroker.session"
        self.__number: str = "0123456789"
        self.__device_id: str = ":".join([str(i) for i in range(11, 17)])
        self.__headers: dict = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        self.__token: str = None
        self.wait: int = 1  # wait 1 second before sending request

    def get_otp(self) -> str:
        """
        Retrieves the OTP for authentication.
        Returns:
            str: The OTP.
        """
        data: dict = {}
        data.update(
            consumerID=self.config.ssi_broker_id,
            consumerSecret=self.config.ssi_broker_secret
        )
        res = request_handler.post(
            url=self.url_otp, headers=self.__headers, data=data, limit=self.wait
        )
        return f"GET {self.url_otp}: {res}"

    def get_token(self) -> str:
        """
        Retrieves the access token for authentication.
        Returns:
            str: The access token.
        """
        if os.path.exists(self.__session_file):
            with open(self.__session_file, "r") as file:
                self.__token = file.read().strip()

        if jwt_handler.is_expired(bearer_token=self.__token):
            print("a")
            data: dict = {}
            data.update(
                consumerID=self.config.ssi_broker_id,
                consumerSecret=self.config.ssi_broker_secret,
                twoFactorType=1,
                code=self.otp,
                isSave=True
            )
            res = request_handler.post(
                url=self.url_auth, headers=self.__headers, data=data, limit=self.wait
            )
            if res.get("status") == 200:
                access_token = " ".join(["Bearer", res.get("data").get("accessToken")])
                print(access_token)
                with open(self.__session_file, "w") as file:
                    file.write(access_token)
            else:
                access_token = None
                print(f"[vBroker] Failed to get access token.: {res}")
            self.__token = access_token
        return self.__token

    def __get_orderbook_history(
        self, account_no: str, from_date: str, to_date: str, wait: int = 1
    ) -> dict:
        """
        Retrieves the order history for a given account within a specified date range.
        Args:
            account_no (str): The account number for which to retrieve the order history.
            from_date (str): The start date of the date range in the format "YYYY-MM-DD".
            to_date (str): The end date of the date range in the format "YYYY-MM-DD".
        Returns:
            dict: The order history data as a dictionary.
        """
        if from_date:
            from_date = datetime.strptime(from_date, "%Y-%m-%d").strftime("%d/%m/%Y")
        if to_date:
            to_date = datetime.strptime(to_date, "%Y-%m-%d").strftime("%d/%m/%Y")
        self.__headers.update({"Authorization": self.get_token()})
        data: dict = {}
        data.update(
            account=account_no,
            startDate=from_date,
            endDate=to_date
        )
        res = request_handler.get(
            url=self.url_order_history, headers=self.__headers, params=data, limit=wait
        )
        if res.get("status") == 200:
            return res.get("data").get("orderHistories")
        else:
            print(f"[vBroker] {res}")
            return []

    def __get_orderbook(self, account_no: str) -> dict:
        """
        Retrieves the orderbook for a specific account.
        Args:
            account_no (str): The account number.
        Returns:
            dict: The orderbook data.
        Raises:
            None
        """
        self.__headers.update({"Authorization": self.get_token()})
        data: dict = {}
        data.update(
            account=account_no
        )
        res = request_handler.get(
            url=self.url_orderbook, headers=self.__headers, params=data, limit=self.wait
        )
        if res.get("status") == 200:
            return res.get("data").get("order")
        else:
            print(f"[vBroker] {res}")
            return []

    def get_max_buy_quantity(self, account_no: str, instrument: str, price: float) -> dict:
        """
        Retrieves the maximum buy quantity for a specific account.
        Args:
            account_no (str): The account number.
        Returns:
            dict: The maximum buy quantity data.
        Raises:
            None
        """
        self.__headers.update({"Authorization": self.get_token()})
        data: dict = {}
        data.update(
            account=account_no,
            instrumentID=instrument,
            price=price
        )
        res = request_handler.get(
            url=self.url_max_buy_quantity, headers=self.__headers, params=data, limit=self.wait
        )
        return res

    def get_max_sell_quantity(self, account_no: str, instrument: str, price: float) -> dict:
        """
        Retrieves the maximum sell quantity for a specific account.
        Args:
            account_no (str): The account number.
        Returns:
            dict: The maximum sell quantity data.
        Raises:
            None
        """
        self.__headers.update({"Authorization": self.get_token()})
        data: dict = {}
        data.update(
            account=account_no,
            instrumentID=instrument,
            price=price
        )
        res = request_handler.get(
            url=self.url_max_sell_quantity, headers=self.__headers, params=data, limit=self.wait
        )
        return res

    # EQUITY
    def __get_equity_positions(self, account_no: str) -> dict:
        """
        Retrieves the equity positions for a given account.
        Args:
            account_no (str): The account number for which to retrieve equity positions.
        Returns:
            dict: A dictionary containing the equity positions.
        Raises:
            None
        """
        self.__headers.update({"Authorization": self.get_token()})
        data: dict = {}
        data.update(
            account=account_no
        )
        res = request_handler.get(
            url=self.url_equity_position, headers=self.__headers, params=data, limit=self.wait
        )
        return res

    def __get_equity_account_balance(self, account_no: str) -> dict:
        """
        Retrieves the equity account balance for a given account.
        Args:
            account_no (str): The account number for which to retrieve the equity account balance.
        Returns:
            dict: A dictionary containing the equity account balance.
        Raises:
            None
        """
        self.__headers.update({"Authorization": self.get_token()})
        data: dict = {}
        data.update(
            account=account_no
        )
        res = request_handler.get(
            url=self.url_equity_account_balance, headers=self.__headers,
            params=data, limit=self.wait
        )
        return res

    def __place_equity_order(
        self,
        account_no: str, side: str, instrument: str, quantity: int, price: float, order_type: str
    ) -> dict:
        data = SSIPlaceOrderRequestModel(
            account=account_no,
            requestID=generate(alphabet=self.__number, size=8),
            instrumentID=instrument,
            market=self.__equity_market_id,
            buySell=side,
            orderType=order_type,
            price=price,
            quantity=quantity,
            deviceId=self.__device_id
        ).model_dump()
        data_signed = sign(json.dumps(data), self.config.ssi_broker_private_key)
        self.__headers.update({
            "Authorization": self.get_token(),
            "X-Signature": data_signed,
        })
        res = request_handler.post(
            url=self.url_equity_new_order, headers=self.__headers, data=data, limit=self.wait
        )
        return res

    def __modify_equity_order(
        self, account_no: str, order_id: str,
        side: str, instrument: str, quantity: int, price: float, order_type: str
    ) -> dict:
        data = SSIModifyOrderRequestModel(
            account=account_no,
            requestID=generate(alphabet=self.__number, size=8),
            orderID=order_id,
            marketID=self.__equity_market_id,
            instrumentID=instrument,
            buySell=side,
            orderType=order_type,
            price=price,
            quantity=quantity,
            deviceId=self.__device_id
        ).model_dump()
        data_signed = sign(json.dumps(data), self.config.ssi_broker_private_key)
        self.__headers.update({
            "Authorization": self.get_token(),
            "X-Signature": data_signed,
        })
        res = request_handler.post(
            url=self.url_equity_modify_order, headers=self.__headers, data=data, limit=self.wait
        )
        return res

    def __cancel_equity_order(
        self, account_no: str, order_id: str, instrument: str, side: str
    ) -> dict:
        data = SSICancelOrderRequestModel(
            account=account_no,
            requestID=generate(alphabet=self.__number, size=8),
            orderID=order_id,
            marketID=self.__equity_market_id,
            instrumentID=instrument,
            buySell=side,
            deviceId=self.__device_id
        ).model_dump()
        data_signed = sign(json.dumps(data), self.config.ssi_broker_private_key)
        self.__headers.update({
            "Authorization": self.get_token(),
            "X-Signature": data_signed,
        })
        res = request_handler.post(
            url=self.url_equity_cancel_order, headers=self.__headers, data=data, limit=self.wait
        )
        return res

    # DERIVATIVES
    def __get_derivative_positions(self, account_no: str) -> dict:
        """
        Retrieves the derivative positions for a given account.
        Args:
            account_no (str): The account number for which to retrieve derivative positions.
        Returns:
            dict: A dictionary containing the derivative positions.
        Raises:
            None
        """
        self.__headers.update({"Authorization": self.get_token()})
        data: dict = {}
        data.update(
            account=account_no,
            querySummary=True
        )
        res = request_handler.get(
            url=self.url_derivative_position, headers=self.__headers, params=data, limit=self.wait
        )
        return res

    def __get_derivative_account_balance(self, account_no: str) -> dict:
        """
        Retrieves the derivative account balance for a given account.
        Args:
            account_no (str): The account number for which to retrieve
                            the derivative account balance.
        Returns:
            dict: A dictionary containing the derivative account balance.
        Raises:
            None
        """
        self.__headers.update({"Authorization": self.get_token()})
        data: dict = {}
        data.update(
            account=account_no
        )
        res = request_handler.get(
            url=self.url_derivative_account_balance, headers=self.__headers,
            params=data, limit=self.wait
        )
        return res

    def __place_derivative_order(
        self,
        account_no: str, side: str, instrument: str, quantity: int, price: float, order_type: str
    ) -> dict:
        data = SSIPlaceOrderRequestModel(
            account=account_no,
            requestID=generate(alphabet=self.__number, size=8),
            instrumentID=instrument,
            market=self.__derivative_market_id,
            buySell=side,
            orderType=order_type,
            price=price,
            quantity=quantity,
            deviceId=self.__device_id
        ).model_dump()
        data_signed = sign(json.dumps(data), self.config.ssi_broker_private_key)
        self.__headers.update({
            "Authorization": self.get_token(),
            "X-Signature": data_signed,
        })
        res = request_handler.post(
            url=self.url_derivative_new_order, headers=self.__headers, data=data, limit=self.wait
        )
        return res

    def __modify_derivative_order(
        self, account_no: str, order_id: str,
        side: str, instrument: str, quantity: int, price: float, order_type: str
    ) -> dict:
        data = SSIModifyOrderRequestModel(
            account=account_no,
            requestID=generate(alphabet=self.__number, size=8),
            orderID=order_id,
            marketID=self.__derivative_market_id,
            instrumentID=instrument,
            buySell=side,
            orderType=order_type,
            price=price,
            quantity=quantity,
            deviceId=self.__device_id
        ).model_dump()
        data_signed = sign(json.dumps(data), self.config.ssi_broker_private_key)
        self.__headers.update({
            "Authorization": self.get_token(),
            "X-Signature": data_signed,
        })
        res = request_handler.post(
            url=self.url_derivative_modify_order, headers=self.__headers, data=data, limit=self.wait
        )
        return res

    def __cancel_derivative_order(
        self, account_no: str, order_id: str, instrument: str, side: str
    ) -> dict:
        data = SSICancelOrderRequestModel(
            account=account_no,
            requestID=generate(alphabet=self.__number, size=8),
            orderID=order_id,
            marketID=self.__derivative_market_id,
            instrumentID=instrument,
            buySell=side,
            deviceId=self.__device_id
        ).model_dump()
        data_signed = sign(json.dumps(data), self.config.ssi_broker_private_key)
        self.__headers.update({
            "Authorization": self.get_token(),
            "X-Signature": data_signed,
        })
        res = request_handler.post(
            url=self.url_derivative_cancel_order, headers=self.__headers, data=data, limit=self.wait
        )
        return res

    def get_ordebbook(self, account_no: str, from_date: str = None, to_date: str = None) -> dict:
        if all([
            from_date is None,
            to_date is None
        ]):
            from_date = to_date = datetime.now().strftime("%Y-%m-%d")
        _orderbook: list = []
        _split_date_range = split_date_range(from_date, to_date) or [(from_date, to_date)]
        for _f_date, _t_date in _split_date_range:
            _order = self.__get_orderbook_history(account_no, _f_date, _t_date, wait=10)
            if _order:
                _orderbook += _order
        return [OrderInfo(**i) for i in _orderbook]

    def get_positions(self, account_no: str, is_equity: bool = True) -> dict:
        if is_equity:
            return self.__get_equity_positions(account_no)
        else:
            return self.__get_derivative_positions(account_no)

    def get_balance(self, account_no: str, is_equity: bool = True) -> dict:
        if is_equity:
            return self.__get_equity_account_balance(account_no)
        else:
            return self.__get_derivative_account_balance(account_no)

    def place_order(
        self, account_no: str, side: str, instrument: str,
        quantity: int, price: float | str, is_equity: bool = True
    ) -> dict:
        if isinstance(price, str):
            order_type = price
            price = 0
        else:
            order_type = "LO"
        side = "B" if side == "BUY" else "S"
        if is_equity:
            return self.__place_equity_order(
                account_no=account_no,
                side=side,
                instrument=instrument,
                quantity=quantity,
                price=price,
                order_type=order_type
            )
        else:
            return self.__place_derivative_order(
                account_no=account_no,
                side=side,
                instrument=instrument,
                quantity=quantity,
                price=price,
                order_type=order_type
            )

    def modify_order(
        self, account_no: str, order_id: str, side: str, instrument: str,
        quantity: int, price: float | str, is_equity: bool = True
    ) -> dict:
        if isinstance(price, str):
            order_type = price
            price = 0
        else:
            order_type = "LO"
        side = "B" if side == "BUY" else "S"
        if is_equity:
            return self.__modify_equity_order(
                account_no=account_no,
                order_id=order_id,
                side=side,
                instrument=instrument,
                quantity=quantity,
                price=price,
                order_type=order_type
            )
        else:
            return self.__modify_derivative_order(
                account_no=account_no,
                order_id=order_id,
                side=side,
                instrument=instrument,
                quantity=quantity,
                price=price,
                order_type=order_type
            )

    def cancel_order(
        self, account_no: str, order_id: str, instrument: str, side: str, is_equity: bool = True
    ) -> dict:
        side = "B" if side == "BUY" else "S"
        if is_equity:
            return self.__cancel_equity_order(
                account_no=account_no,
                order_id=order_id,
                instrument=instrument,
                side=side
            )
        else:
            return self.__cancel_derivative_order(
                account_no=account_no,
                order_id=order_id,
                instrument=instrument,
                side=side
            )
