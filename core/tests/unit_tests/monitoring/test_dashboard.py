import unittest
from unittest.mock import patch, Mock
from core.monitoring.dashboard import MonitoringDashboard  
import requests

class TestMonitoringDashboard(unittest.TestCase):

    def setUp(self):
        # Example nodes for testing
        self.nodes = [("localhost", 8545), ("localhost", 8546)]
        self.dashboard = MonitoringDashboard(nodes=self.nodes, polling_interval=10)

    @patch('requests.get')
    def test_fetch_node_status_success(self, mock_get):
        """Test fetch_node_status when the request is successful."""
        # Mock response for a successful status request
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"status": "active"}
        mock_get.return_value = mock_response

        result = self.dashboard.fetch_node_status("localhost", 8545)
        self.assertEqual(result, {"status": "active"})
        mock_get.assert_called_once_with("http://localhost:8545/status", timeout=5)

    @patch('requests.get')
    def test_fetch_node_status_failure(self, mock_get):
        """Test fetch_node_status when the request fails."""
        # Mock a RequestException to simulate a failure
        mock_get.side_effect = requests.exceptions.RequestException("Connection error")

        result = self.dashboard.fetch_node_status("localhost", 8545)
        self.assertEqual(result, {"error": "Connection error"})
        mock_get.assert_called_once_with("http://localhost:8545/status", timeout=5)

    @patch('requests.get')
    def test_fetch_node_metrics_success(self, mock_get):
        """Test fetch_node_metrics when the request is successful."""
        # Mock response for a successful metrics request
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"metrics": {"cpu_usage": "70%"}}
        mock_get.return_value = mock_response

        result = self.dashboard.fetch_node_metrics("localhost", 8545)
        self.assertEqual(result, {"metrics": {"cpu_usage": "70%"}})
        mock_get.assert_called_once_with("http://localhost:8545/metrics", timeout=5)

    @patch('requests.get')
    def test_fetch_node_metrics_failure(self, mock_get):
        """Test fetch_node_metrics when the request fails."""
        # Mock a RequestException to simulate a failure
        mock_get.side_effect = requests.exceptions.RequestException("Connection error")

        result = self.dashboard.fetch_node_metrics("localhost", 8545)
        self.assertEqual(result, {"error": "Connection error"})
        mock_get.assert_called_once_with("http://localhost:8545/metrics", timeout=5)

    @patch('core.monitoring.dashboard.MonitoringDashboard.fetch_node_status')
    @patch('core.monitoring.dashboard.MonitoringDashboard.fetch_node_metrics')
    @patch('streamlit.write')
    @patch('streamlit.table')
    @patch('streamlit.title')
    def test_run_dashboard(self, mock_title, mock_table, mock_write, mock_fetch_node_metrics, mock_fetch_node_status):
        """Test that run_dashboard fetches data and updates Streamlit UI."""
        # Mocking the return values for node status and metrics
        mock_fetch_node_status.return_value = {"status": "active"}
        mock_fetch_node_metrics.return_value = {"metrics": {"cpu_usage": "70%"}}

        # Run the dashboard method
        self.dashboard.run_dashboard()

        # Verify that fetch_node_status was called for each node
        mock_fetch_node_status.assert_any_call("localhost", 8545)
        mock_fetch_node_status.assert_any_call("localhost", 8546)

        # Verify that fetch_node_metrics was called for each node
        mock_fetch_node_metrics.assert_any_call("localhost", 8545)
        mock_fetch_node_metrics.assert_any_call("localhost", 8546)

        # Ensure Streamlit functions were called
        mock_title.assert_called_once_with("Blockchain Monitoring Dashboard")
        self.assertEqual(mock_table.call_count, 2)  # Once for status, once for metrics
        mock_write.assert_called()


if __name__ == '__main__':
    unittest.main()
