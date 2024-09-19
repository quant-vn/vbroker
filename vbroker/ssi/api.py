import json
from datetime import datetime

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

from ..interface_broker_api import IBrokerAPI
from ..utils import jwt_handler, request_handler, sign


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
        if jwt_handler.is_expired(bearer_token=self.__token):
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
            else:
                access_token = None
            self.__token = access_token
        return self.__token

    def get_order_history(self, account_no: str, from_date: str, to_date: str) -> dict:
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
            url=self.url_order_history, headers=self.__headers, params=data, limit=self.wait
        )
        return res

    def get_orderbook(self, account_no: str) -> dict:
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
        return res

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
    def get_equity_positions(self, account_no: str) -> dict:
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

    def get_equity_account_balance(self, account_no: str) -> dict:
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

    def place_equity_order(
        self, account_no: str, side: str, instrument: str, quantity: int, price: float
    ) -> dict:
        data: dict = {}
        data.update(
            account=account_no,
            requestID="25",
            instrumentID=instrument,
            market="VN",
            buySell='B' if side == 'BUY' else 'S',
            orderType="LO",
            price=3300,
            quantity=quantity,
            stopOrder=False,
            stopPrice=0.0,
            stopType='',
            stopStep=0.0,
            lossStep=0.0,
            profitStep=0.0,
            channelID='TA',
            code='',
            deviceId=":".join([str(i) for i in range(11, 17)]),
            userAgent=''
        )
        data_signed = sign(json.dumps(data), self.config.ssi_broker_private_key)
        self.__headers.update({
            "Authorization": self.get_token(),
            "X-Signature": data_signed,
        })
        res = request_handler.post(
            url=self.url_equity_new_order, headers=self.__headers, data=data, limit=self.wait
        )
        return res

    def modify_equity_order(
        self, account_no: str, order_id: str,
        side: str, instrument: str, quantity: int, price: float
    ) -> dict:
        data: dict = {}
        data.update(
            account=account_no,
            requestID="MODIFY1",
            orderID=order_id,
            marketID="VN",
            instrumentID=instrument,
            price=300,
            quantity=quantity,
            buySell='B' if side == 'BUY' else 'S',
            orderType="LO",
            code="",
            deviceId=":".join([str(i) for i in range(11, 17)]),
            userAgent=""
        )
        data_signed = sign(json.dumps(data), self.config.ssi_broker_private_key)
        self.__headers.update({
            "Authorization": self.get_token(),
            "X-Signature": data_signed,
        })
        res = request_handler.post(
            url=self.url_equity_modify_order, headers=self.__headers, data=data, limit=self.wait
        )
        return res

    def cancel_equity_order(
        self, account_no: str, order_id: str, instrument: str, side: str
    ) -> dict:
        data: dict = {}
        data.update(
            account=account_no,
            requestID="CANCEL1",
            orderID=order_id,
            marketID="VN",
            instrumentID=instrument,
            buySell='B' if side == 'BUY' else 'S',
            code="",
            deviceId=":".join([str(i) for i in range(11, 17)]),
            userAgent=""
        )
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
    def get_derivative_positions(self, account_no: str) -> dict:
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

    def get_derivative_account_balance(self, account_no: str) -> dict:
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

    def place_derivative_order(
        self, account_no: str, side: str, instrument: str, quantity: int, price: float
    ) -> dict:
        data: dict = {}
        data.update(
            account=account_no,
            requestID="26",
            instrumentID=instrument,
            market="VNFE",
            buySell='B' if side == 'BUY' else 'S',
            orderType="MTL",
            price=0,
            quantity=quantity,
            stopOrder=False,
            stopPrice=0.0,
            stopType='',
            stopStep=0.0,
            lossStep=0.0,
            profitStep=0.0,
            channelID='TA',
            code='',
            deviceId=":".join([str(i) for i in range(11, 17)]),
            userAgent=''
        )
        data_signed = sign(json.dumps(data), self.config.ssi_broker_private_key)
        self.__headers.update({
            "Authorization": self.get_token(),
            "X-Signature": data_signed,
        })
        res = request_handler.post(
            url=self.url_derivative_new_order, headers=self.__headers, data=data, limit=self.wait
        )
        return res

    def modify_derivative_order(
        self, account_no: str, order_id: str,
        side: str, instrument: str, quantity: int, price: float
    ) -> dict:
        data: dict = {}
        data.update(
            account=account_no,
            requestID="MODIFY2",
            orderID=order_id,
            marketID="VNFE",
            instrumentID=instrument,
            price=0,
            quantity=quantity,
            buySell='B' if side == 'BUY' else 'S',
            orderType="MTL",
            code="",
            deviceId=":".join([str(i) for i in range(11, 17)]),
            userAgent=""
        )
        data_signed = sign(json.dumps(data), self.config.ssi_broker_private_key)
        self.__headers.update({
            "Authorization": self.get_token(),
            "X-Signature": data_signed,
        })
        res = request_handler.post(
            url=self.url_derivative_modify_order, headers=self.__headers, data=data, limit=self.wait
        )
        return res

    def cancel_derivative_order(
        self, account_no: str, order_id: str, instrument: str, side: str
    ) -> dict:
        data: dict = {}
        data.update(
            account=account_no,
            requestID="CANCEL2",
            orderID=order_id,
            marketID="VNFE",
            instrumentID=instrument,
            buySell='B' if side == 'BUY' else 'S',
            code="",
            deviceId=":".join([str(i) for i in range(11, 17)]),
            userAgent=""
        )
        data_signed = sign(json.dumps(data), self.config.ssi_broker_private_key)
        self.__headers.update({
            "Authorization": self.get_token(),
            "X-Signature": data_signed,
        })
        res = request_handler.post(
            url=self.url_derivative_cancel_order, headers=self.__headers, data=data, limit=self.wait
        )
        return res
