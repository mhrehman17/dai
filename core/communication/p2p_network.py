import socket
import threading
import logging
from typing import List, Tuple, Dict

class P2PNetwork:
    def __init__(self, host: str, port: int, peers: List[Tuple[str, int]], logger: logging.Logger = None):
        """
        Initializes a peer-to-peer network for decentralized communication.
        :param host: The hostname or IP address to bind the server.
        :param port: The port on which the server will listen.
        :param peers: A list of peer addresses in the format (host, port).
        :param logger: Logger instance to log network activities.
        """
        self.host = host
        self.port = port
        self.peers = peers
        self.logger = logger or logging.getLogger(__name__)
        self.running = False
        self.server_socket = None

    def start_network(self):
        """
        Starts the P2P network, allowing peers to connect.
        """
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(5)
            self.running = True
            self.logger.info(f"P2P Network started at {self.host}:{self.port}")
            threading.Thread(target=self._accept_connections, daemon=True).start()
        except Exception as e:
            self.logger.error(f"Failed to start P2P network: {e}")

    def stop_network(self):
        """
        Stops the P2P network, closing all connections.
        """
        self.running = False
        if self.server_socket:
            self.server_socket.close()
            self.logger.info("P2P Network stopped.")

    def _accept_connections(self):
        """
        Accepts incoming peer connections and starts a new thread for each connection.
        """
        while self.running:
            try:
                client_socket, client_address = self.server_socket.accept()
                self.logger.info(f"Connection accepted from {client_address}")
                threading.Thread(target=self._handle_peer, args=(client_socket, client_address), daemon=True).start()
            except Exception as e:
                self.logger.error(f"Error accepting connections: {e}")
                break

    def _handle_peer(self, client_socket: socket.socket, client_address: Tuple[str, int]):
        """
        Handles communication with a connected peer.
        :param client_socket: The socket connected to the peer.
        :param client_address: The address of the connected peer.
        """
        with client_socket:
            while self.running:
                try:
                    data = client_socket.recv(1024)
                    if not data:
                        self.logger.info(f"Connection closed by {client_address}")
                        break
                    message = data.decode('utf-8')
                    self.logger.info(f"Received message from {client_address}: {message}")
                    # Echo the received message back to the sender (simple handling for now)
                    client_socket.sendall(data)
                except Exception as e:
                    self.logger.error(f"Error handling peer {client_address}: {e}")
                    break

    def send_message_to_peer(self, peer_address: Tuple[str, int], message: str):
        """
        Sends a message to a specific peer.
        :param peer_address: The address of the peer to send the message to.
        :param message: The message to be sent.
        """
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as peer_socket:
                peer_socket.connect(peer_address)
                peer_socket.sendall(message.encode('utf-8'))
                self.logger.info(f"Message sent to {peer_address}: {message}")
                # Optionally receive an acknowledgment
                response = peer_socket.recv(1024).decode('utf-8')
                self.logger.info(f"Acknowledgment received from {peer_address}: {response}")
        except Exception as e:
            self.logger.error(f"Failed to send message to {peer_address}: {e}")

# Example usage
if __name__ == "__main__":
    # Set up logger
    p2p_logger = logging.getLogger("p2p_network")
    p2p_logger.setLevel(logging.INFO)
    console_handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)
    p2p_logger.addHandler(console_handler)

    # Initialize P2P Network
    p2p_network = P2PNetwork(host="localhost", port=5000, peers=[("localhost", 5001)], logger=p2p_logger)
    p2p_network.start_network()

    # Allow some time for demonstration purposes
    try:
        threading.Event().wait(10)
    finally:
        p2p_network.stop_network()
