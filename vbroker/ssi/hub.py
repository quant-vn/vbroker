import json
import asyncio
import random
from urllib.parse import urlencode

from .constant import HUB_URL, HUB
from .enum import SSIOrderStatusEnum, SSISideEnum
from ..interface_broker_hub import IBrokerHUB
from ..utils import SocketListener, request_handler, convert_timestamp_to_datetime
from ..model import vBrokerOrder
from ..enum_broker import OrderStatusEnum, SideEnum


class SSIBrokerHUB(IBrokerHUB):
    def __init__(self, api):
        super().__init__(api)
        self.url: str = HUB_URL.replace("wss", "https")
        self.url_hub: str = HUB_URL
        self.message_send_to_socket: dict = {
            "H": HUB,
            "M": "SwitchChannels",
            "I": 0,
        }
        # Reconnection settings
        self.max_reconnect_attempts = 5
        self.base_delay = 1  # Base delay in seconds
        self.max_delay = 60  # Maximum delay between reconnection attempts

    def generate_socket_url(self):
        """
        Generates the socket URL for the connection.
        Returns:
            str: The socket URL.
        """
        self.connection_data: dict = {
            "connectionData": '[{"name": "' + HUB + '"}]',
            "clientProtocol": '1.3'
        }
        self.negotiate_query = urlencode(self.connection_data)
        self.url_negotiate = f"{self.url}/negotiate?{self.negotiate_query}"
        response = request_handler.post(self.url_negotiate, headers=self.headers)
        query = urlencode({
            "transport": "webSockets",
            "connectionToken": response["ConnectionToken"],
            "connectionData": '[{"name": "' + HUB + '"}]',
            "clientProtocol": response["ProtocolVersion"],
        })
        socket_url = f"{self.url_hub}/connect?{query}"
        return socket_url

    def calculate_backoff_delay(self, attempt):
        """
        Calculate exponential backoff delay with jitter.
        Args:
            attempt (int): Current reconnection attempt number.
        Returns:
            float: Delay in seconds before next reconnection attempt.
        """
        # Exponential backoff with full jitter
        delay = min(self.max_delay, self.base_delay * (2 ** attempt))
        jitter = random.uniform(0, delay)
        return jitter

    async def listen(self, on_message):
        """
        Listens for messages from the socket server with automatic reconnection.
        Args:
            on_message: The callback function to handle incoming messages.
        """
        self.headers: dict = {
            "Authorization": self.api.get_token(),
        }
        for attempt in range(self.max_reconnect_attempts):
            try:
                socket = SocketListener()
                async with socket.connect_socket_server(
                    self.generate_socket_url(), self.headers
                ) as websocket:
                    print(f"[vBroker] WebSocket connected (Attempt {attempt + 1})")
                    self.max_reconnect_attempts = 5
                    async for msg in websocket:
                        try:
                            msg = json.loads(msg)
                            if "M" not in msg:
                                continue
                            for i in msg["M"]:
                                if "A" not in i or not len(i["A"]):
                                    continue
                                msg = json.loads(i["A"][0])
                                if not msg.get("data"):
                                    continue
                                message = msg.get("data").get("message")
                                if msg.get("data").get("orderStatus"):
                                    _raw_status = msg.get("data").get("orderStatus")
                                    status = OrderStatusEnum[SSIOrderStatusEnum[_raw_status].value]
                                    if not message:
                                        message = _raw_status
                                    cancelled_quantity = msg.get("data").get("cancelQty", 0)
                                else:
                                    status = OrderStatusEnum.REJECTED
                                    cancelled_quantity = msg.get("data").get("quantity")
                                on_message(vBrokerOrder(
                                    account_no=msg.get("data").get("account"),
                                    order_id=msg.get("data").get("orderID"),
                                    unique_id=msg.get("data").get("origRequestID"),
                                    instrument=msg.get("data").get("instrumentID"),
                                    side=SideEnum[
                                        SSISideEnum[msg.get("data").get("buySell")].value
                                    ],
                                    order_type='',
                                    price=msg.get("data").get("price", 0),
                                    avg_price=msg.get("data").get("avgPrice", 0),
                                    quantity=msg.get("data").get("quantity"),
                                    filled_quantity=msg.get("data").get("filledQty", 0),
                                    os_quantity=msg.get("data").get("osQty", 0),
                                    cancelled_quantity=cancelled_quantity,
                                    status=status,
                                    input_time=convert_timestamp_to_datetime(
                                        int(msg.get("data").get("inputTime"))/1000
                                    ),
                                    modified_time=convert_timestamp_to_datetime(
                                        int(msg.get("data").get("modifiedTime"))/1000
                                    ),
                                    message=message
                                ))
                        except Exception as e:
                            print(f"[vBroker] Message processing error: {e}")

            except Exception as e:
                print(f"[vBroker] Connection error: {e}")
                # If this was the last attempt, raise the exception
                if attempt == self.max_reconnect_attempts - 1:
                    raise
                # Calculate backoff delay
                delay = self.calculate_backoff_delay(attempt)
                print(f"[vBroker] Reconnecting in {delay:.2f} seconds...")
                # Wait before trying to reconnect
                await asyncio.sleep(delay)
        print("[vBroker] Maximum reconnection attempts reached")
