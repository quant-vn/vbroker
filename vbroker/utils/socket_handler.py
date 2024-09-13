""" This module is responsible for handling the socket connection to the server. """
import websockets


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
