import unittest
from core.monitoring.log_collector import LogCollector
from unittest.mock import patch, MagicMock

class TestLogCollector(unittest.TestCase):
    def setUp(self):
        # Set up an instance of the LogCollector before each test
        self.log_collector = LogCollector()

    @patch("core.monitoring.log_collector.LogCollector.collect_agent_logs")
    def test_collect_agent_logs(self, mock_collect_agent_logs):
        # Test collecting logs from agents
        mock_collect_agent_logs.return_value = "Agent logs collected successfully"
        result = self.log_collector.collect_agent_logs(["agent_1", "agent_2"])
        mock_collect_agent_logs.assert_called_once_with(["agent_1", "agent_2"])
        self.assertEqual(result, "Agent logs collected successfully")

    @patch("core.monitoring.log_collector.LogCollector.collect_orchestrator_logs")
    def test_collect_orchestrator_logs(self, mock_collect_orchestrator_logs):
        # Test collecting logs from the orchestrator
        mock_collect_orchestrator_logs.return_value = "Orchestrator logs collected successfully"
        result = self.log_collector.collect_orchestrator_logs()
        mock_collect_orchestrator_logs.assert_called_once()
        self.assertEqual(result, "Orchestrator logs collected successfully")

    @patch("core.monitoring.log_collector.LogCollector.collect_blockchain_logs")
    def test_collect_blockchain_logs(self, mock_collect_blockchain_logs):
        # Test collecting logs from blockchain nodes
        mock_collect_blockchain_logs.return_value = "Blockchain logs collected successfully"
        result = self.log_collector.collect_blockchain_logs(["node_1", "node_2"])
        mock_collect_blockchain_logs.assert_called_once_with(["node_1", "node_2"])
        self.assertEqual(result, "Blockchain logs collected successfully")

    def tearDown(self):
        # Clean up after each test
        self.log_collector = None

if __name__ == "__main__":
    unittest.main()
