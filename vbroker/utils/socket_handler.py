""" This module is responsible for handling the socket connection to the server. """
import json
import asyncio
import itertools
import websockets
from websockets.exceptions import ConnectionClosed


async def keepalive(websocket: websockets.WebSocketClientProtocol, ping_interval: int = 30):
    """
    Sends periodic ping messages to the given websocket to keep the connection alive.

    Args:
        websocket (WebSocket): The websocket connection to keep alive.
        ping_interval (int, optional): The interval in seconds between each ping message.
                                       Defaults to 30.

    Raises:
        ConnectionClosed: If the websocket connection is closed.
    """
    for ping in itertools.count():
        await asyncio.sleep(ping_interval)
        try:
            await websocket.send(json.dumps({"ping": ping}))
        except ConnectionClosed:
            break


class SocketListener:
    """
    A class that handles socket connections.
    Methods:
    --------
    connect_socket_server(url: str, headers: dict) -> websockets.WebSocketClientProtocol:
        Connects to a socket server using the specified URL and headers.
    """
    def connect_socket_server(self, url: str, headers: dict) -> websockets.WebSocketClientProtocol:
        """
        Connects to a socket server using the specified URL and headers.
        Parameters:
        -----------
        url : str
            The URL of the socket server to connect to.
        headers : dict
            Additional headers to include in the connection request.
        Returns:
        --------
        websockets.WebSocketClientProtocol
            The WebSocket client protocol object representing the connection.
        """
        return websockets.connect(url, extra_headers=headers)
