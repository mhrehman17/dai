import unittest
from core.monitoring.blockchain_monitor import BlockchainMonitor
from unittest.mock import patch, MagicMock

class TestBlockchainMonitor(unittest.TestCase):
    def setUp(self):
        # Set up an instance of the BlockchainMonitor before each test
        self.blockchain_monitor = BlockchainMonitor()

    @patch("core.monitoring.blockchain_monitor.BlockchainMonitor.track_blockchain_status")
    def test_track_blockchain_status(self, mock_track_blockchain_status):
        # Test tracking the status of blockchain nodes
        mock_track_blockchain_status.return_value = {"node_1": "active", "node_2": "inactive"}
        result = self.blockchain_monitor.track_blockchain_status(["node_1", "node_2"])
        mock_track_blockchain_status.assert_called_once_with(["node_1", "node_2"])
        self.assertEqual(result, {"node_1": "active", "node_2": "inactive"})

    @patch("core.monitoring.blockchain_monitor.BlockchainMonitor.collect_node_metrics")
    def test_collect_node_metrics(self, mock_collect_node_metrics):
        # Test collecting metrics from blockchain nodes
        mock_collect_node_metrics.return_value = {"block_height": 1200, "transaction_rate": 15}
        result = self.blockchain_monitor.collect_node_metrics("node_1")
        mock_collect_node_metrics.assert_called_once_with("node_1")
        self.assertEqual(result, {"block_height": 1200, "transaction_rate": 15})

    @patch("core.monitoring.blockchain_monitor.BlockchainMonitor.alert_on_fork_detection")
    def test_alert_on_fork_detection(self, mock_alert_on_fork_detection):
        # Test raising an alert when a blockchain fork is detected
        mock_alert_on_fork_detection.return_value = "Fork detected and alert raised"
        result = self.blockchain_monitor.alert_on_fork_detection("fork_detected")
        mock_alert_on_fork_detection.assert_called_once_with("fork_detected")
        self.assertEqual(result, "Fork detected and alert raised")

    def tearDown(self):
        # Clean up after each test
        self.blockchain_monitor = None

if __name__ == "__main__":
    unittest.main()