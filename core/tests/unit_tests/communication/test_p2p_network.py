import unittest
from unittest.mock import patch, MagicMock
import socket
import threading
import logging
from core.communication.p2p_network import P2PNetwork  # Assuming the file is named p2p_network.py

class TestP2PNetwork(unittest.TestCase):

    def setUp(self):
        # Set up logger for the tests
        self.logger = logging.getLogger("test_p2p_network")
        self.logger.setLevel(logging.INFO)
        console_handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

        # Set up the P2P network for testing
        self.p2p_network = P2PNetwork(host="localhost", port=5000, peers=[("localhost", 5001)], logger=self.logger)

    @patch('socket.socket')
    def test_start_network(self, mock_socket):
        # Test starting the P2P network
        mock_socket_instance = MagicMock()
        mock_socket.return_value = mock_socket_instance

        self.p2p_network.start_network()
        mock_socket_instance.bind.assert_called_with(("localhost", 5000))
        mock_socket_instance.listen.assert_called_once()
        self.assertTrue(self.p2p_network.running)
        self.logger.info("test_start_network passed")

    @patch('socket.socket')
    def test_stop_network(self, mock_socket):
        # Test stopping the P2P network
        self.p2p_network.running = True
        mock_socket_instance = MagicMock()
        mock_socket.return_value = mock_socket_instance
        self.p2p_network.server_socket = mock_socket_instance

        self.p2p_network.stop_network()
        mock_socket_instance.close.assert_called_once()
        self.assertFalse(self.p2p_network.running)
        self.logger.info("test_stop_network passed")

    @patch('socket.socket')
    def test_accept_connections(self, mock_socket):
        # Test accepting incoming connections
        mock_socket_instance = MagicMock()
        mock_socket.return_value = mock_socket_instance

        self.p2p_network.start_network()
        mock_socket_instance.accept.return_value = (mock_socket_instance, ("localhost", 5001))

        with patch.object(self.p2p_network, '_handle_peer', return_value=None) as mock_handle_peer:
            threading.Thread(target=self.p2p_network._accept_connections, daemon=True).start()
            threading.Event().wait(1)  # Allow some time for the thread to start
            mock_handle_peer.assert_called_with(mock_socket_instance, ("localhost", 5001))
            self.logger.info("test_accept_connections passed")

    @patch('socket.socket')
    def test_handle_peer(self, mock_socket):
        # Test handling peer communication
        mock_socket_instance = MagicMock()
        mock_socket.return_value = mock_socket_instance
        mock_socket_instance.recv.return_value = b"Hello from peer"

        self.p2p_network.running = True

        with patch.object(mock_socket_instance, 'sendall') as mock_sendall:
            self.p2p_network._handle_peer(mock_socket_instance, ("localhost", 5001))
            mock_socket_instance.recv.assert_called_once()
            mock_sendall.assert_called_with(b"Hello from peer")
            self.logger.info("test_handle_peer passed")

    @patch('socket.socket')
    def test_send_message_to_peer_success(self, mock_socket):
        # Test sending a message to a peer successfully
        mock_socket_instance = MagicMock()
        mock_socket.return_value = mock_socket_instance
        mock_socket_instance.recv.return_value = b"Acknowledgment"

        self.p2p_network.send_message_to_peer(("localhost", 5001), "Hello Peer")
        mock_socket_instance.connect.assert_called_with(("localhost", 5001))
        mock_socket_instance.sendall.assert_called_with(b"Hello Peer")
        mock_socket_instance.recv.assert_called_once()
        self.logger.info("test_send_message_to_peer_success passed")

    @patch('socket.socket')
    def test_send_message_to_peer_failure(self, mock_socket):
        # Test failing to send a message to a peer
        mock_socket_instance = MagicMock()
        mock_socket.return_value = mock_socket_instance
        mock_socket_instance.connect.side_effect = socket.error("Connection failed")

        with self.assertLogs(self.logger, level='ERROR') as log:
            self.p2p_network.send_message_to_peer(("localhost", 5001), "Hello Peer")
            self.assertIn("Failed to send message to ('localhost', 5001): Connection failed", log.output[-1])
            self.logger.info("test_send_message_to_peer_failure passed")

if __name__ == '__main__':
    unittest.main()
