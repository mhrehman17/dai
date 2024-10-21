import unittest
from unittest.mock import patch, Mock, MagicMock
import logging
import requests
import time
from core.monitoring.orchestrator_monitor import OrchestratorMonitor  # Assuming the class is in a file named orchestrator_monitor.py


class TestOrchestratorMonitor(unittest.TestCase):
    def setUp(self):
        # Example nodes for testing
        self.orchestrator_nodes = [
            ("localhost", 8080),
            ("localhost", 8081)
        ]
        # Create a mock logger
        self.logger = MagicMock(spec=logging.Logger)
        # Initialize OrchestratorMonitor
        self.monitor = OrchestratorMonitor(
            orchestrator_nodes=self.orchestrator_nodes,
            polling_interval=5,
            logger=self.logger
        )

    @patch("requests.get")
    def test_monitor_nodes_successful_response(self, mock_get):
        """Test that orchestrator nodes return a successful response."""
        # Mock response for a successful status request
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"status": "active"}
        mock_get.return_value = mock_response

        # Run one cycle of node monitoring
        with patch("time.sleep", return_value=None):
            self.monitor._monitor_nodes()

        # Ensure that the correct URL was used and logger called
        mock_get.assert_any_call("http://localhost:8080/orchestrator_status", timeout=5)
        mock_get.assert_any_call("http://localhost:8081/orchestrator_status", timeout=5)
        self.logger.info.assert_any_call("Orchestrator at localhost:8080 is active. Status: {'status': 'active'}")
        self.logger.info.assert_any_call("Orchestrator at localhost:8081 is active. Status: {'status': 'active'}")

    @patch("requests.get")
    def test_monitor_nodes_unsuccessful_response(self, mock_get):
        """Test that orchestrator nodes handle unsuccessful responses correctly."""
        # Mock response with a non-200 status code
        mock_response = Mock()
        mock_response.status_code = 500
        mock_get.return_value = mock_response

        # Run one cycle of node monitoring
        with patch("time.sleep", return_value=None):
            self.monitor._monitor_nodes()

        # Ensure that the warning logger was called
        self.logger.warning.assert_any_call("Orchestrator at localhost:8080 responded with status code 500")
        self.logger.warning.assert_any_call("Orchestrator at localhost:8081 responded with status code 500")

    @patch("requests.get")
    def test_monitor_nodes_request_exception(self, mock_get):
        """Test that orchestrator nodes handle request exceptions properly."""
        # Mock a request exception
        mock_get.side_effect = requests.exceptions.RequestException("Connection error")

        # Run one cycle of node monitoring
        with patch("time.sleep", return_value=None):
            self.monitor._monitor_nodes()

        # Ensure that the error logger was called
        self.logger.error.assert_any_call("Failed to reach orchestrator at localhost:8080: Connection error")
        self.logger.error.assert_any_call("Failed to reach orchestrator at localhost:8081: Connection error")

    @patch("requests.get")
    def test_log_node_metrics_successful(self, mock_get):
        """Test that metrics are logged successfully for each orchestrator node."""
        # Mock response for a successful metrics request
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = "CPU Usage: 45%\nMemory Usage: 60%"
        mock_get.return_value = mock_response

        # Log node metrics
        self.monitor.log_node_metrics()

        # Ensure that the correct URLs were used and logger called
        mock_get.assert_any_call("http://localhost:8080/orchestrator_metrics", timeout=5)
        mock_get.assert_any_call("http://localhost:8081/orchestrator_metrics", timeout=5)
        self.logger.info.assert_any_call("Metrics for orchestrator at localhost:8080: CPU Usage: 45%\nMemory Usage: 60%")
        self.logger.info.assert_any_call("Metrics for orchestrator at localhost:8081: CPU Usage: 45%\nMemory Usage: 60%")

    @patch("requests.get")
    def test_log_node_metrics_unsuccessful(self, mock_get):
        """Test that unsuccessful metrics retrieval is handled correctly."""
        # Mock response with a non-200 status code
        mock_response = Mock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        # Log node metrics
        self.monitor.log_node_metrics()

        # Ensure that the warning logger was called
        self.logger.warning.assert_any_call("Failed to get metrics for orchestrator at localhost:8080, status code 404")
        self.logger.warning.assert_any_call("Failed to get metrics for orchestrator at localhost:8081, status code 404")

    @patch("requests.get")
    def test_monitor_nodes_boundary_conditions(self, mock_get):
        """Test boundary conditions for orchestrator node monitoring."""
        # Test with an empty orchestrator nodes list
        monitor = OrchestratorMonitor(orchestrator_nodes=[], polling_interval=5, logger=self.logger)
        with patch("time.sleep", return_value=None):
            monitor._monitor_nodes()
        # Ensure no requests are made and no logs are generated
        mock_get.assert_not_called()
        self.logger.info.assert_not_called()
        self.logger.warning.assert_not_called()
        self.logger.error.assert_not_called()

    @patch("requests.get")
    def test_log_node_metrics_request_exception(self, mock_get):
        """Test that metrics retrieval handles request exceptions properly."""
        # Mock a request exception
        mock_get.side_effect = requests.exceptions.RequestException("Metrics connection error")

        # Log node metrics
        self.monitor.log_node_metrics()

        # Ensure that the error logger was called
        self.logger.error.assert_any_call("Failed to get metrics from orchestrator at localhost:8080: Metrics connection error")
        self.logger.error.assert_any_call("Failed to get metrics from orchestrator at localhost:8081: Metrics connection error")

    def test_start_stop_monitoring(self):
        """Test starting and stopping the monitoring process."""
        with patch("time.sleep", return_value=None):
            # Start the monitoring process
            self.monitor.start_monitoring()
            time.sleep(0.1)  # Let the thread start
            self.monitor.stop_monitoring()

            # Ensure the correct log messages were made
            self.logger.info.assert_any_call("Orchestrator monitoring started.")
            self.logger.info.assert_any_call("Orchestrator monitoring stopped.")

    def test_polling_interval_boundaries(self):
        """Test boundary conditions for polling intervals."""
        # Test with polling interval set to zero
        monitor = OrchestratorMonitor(orchestrator_nodes=self.orchestrator_nodes, polling_interval=0, logger=self.logger)
        self.assertEqual(monitor.polling_interval, 0)

        # Test with a very large polling interval
        large_interval = 10**6
        monitor = OrchestratorMonitor(orchestrator_nodes=self.orchestrator_nodes, polling_interval=large_interval, logger=self.logger)
        self.assertEqual(monitor.polling_interval, large_interval)


if __name__ == "__main__":
    unittest.main()
