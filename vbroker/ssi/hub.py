""" HUB broker for SSI """
import json
from urllib.parse import urlencode

from .constant import HUB_URL, HUB
from ..interface_broker_hub import IBrokerHUB
from ..utils import SocketListener, request_handler


class SSIBrokerHUB(IBrokerHUB):
    def __init__(self, api):
        super().__init__(api)
        self.url: str = HUB_URL.replace("wss", "https")
        self.url_hub: str = HUB_URL
        self.headers: dict = {
            "Authorization": self.api.get_token(),
        }
        self.stream_url = self.generate_socket_url()
        self.message_send_to_socket: dict = {
            "H": HUB,
            "M": "SwitchChannels",
            "I": 0,
        }

    def generate_socket_url(self):
        """
        Generates the socket URL for the connection.
        Returns:
            str: The socket URL.
        """
        self.connection_data: dict = {
            "connectionData": '[{"name": "' + HUB + '"}]',
            "clientProtocol": '1.5'
        }
        print(self.connection_data)
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

    async def listen(self, on_message):
        """
        Listens for messages from the socket server.
        Args:
            args: The arguments for the listen function.
            on_message: The callback function to handle incoming messages.
        """
        try:
            socket = SocketListener()
            async with socket.connect_socket_server(self.stream_url, self.headers) as websocket:
                async for msg in websocket:
                    try:
                        msg = json.loads(msg)
                        if "M" not in msg:
                            continue
                        for i in msg["M"]:
                            if "A" not in i or not len(i["A"]):
                                continue
                            msg = json.loads(i["A"][0])
                            on_message(msg)
                    except Exception as e:
                        print(f" Connection error: {e}")
        except Exception as e:
            print(f" Connection error: {e}")
