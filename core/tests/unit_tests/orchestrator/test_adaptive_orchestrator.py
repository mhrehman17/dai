import unittest
from unittest.mock import patch, MagicMock
from core.orchestrator.adaptive_orchestrator import AdaptiveOrchestrator  # Assuming the original code is saved as adaptive_orchestrator.py
import logging
import time

class TestAdaptiveOrchestrator(unittest.TestCase):

    def setUp(self):
        """Set up common test assets."""
        self.logger = logging.getLogger("test_logger")
        self.nodes = [
            {"host": "localhost", "id": "node_1"},
            {"host": "localhost", "id": "node_2"},
            {"host": "localhost", "id": "node_3"}
        ]
        self.orchestrator = AdaptiveOrchestrator(nodes=self.nodes, polling_interval=1, logger=self.logger)

    def tearDown(self):
        """Ensure any orchestrating threads are stopped after each test."""
        self.orchestrator.stop_orchestrating()

    @patch.object(AdaptiveOrchestrator, '_fetch_node_resources')
    def test_start_and_stop_orchestrating(self, mock_fetch_resources):
        """Test that orchestrating starts and stops correctly."""
        mock_fetch_resources.return_value = {
            "cpu_usage": "10%",
            "memory_available": "4GB",
            "network_bandwidth": "20Mbps"
        }
        
        self.orchestrator.start_orchestrating()
        time.sleep(2)
        self.assertTrue(self.orchestrator.running, "Orchestrator should be running after start.")

        self.orchestrator.stop_orchestrating()
        time.sleep(1)
        self.assertFalse(self.orchestrator.running, "Orchestrator should be stopped after calling stop_orchestrating.")

    @patch.object(AdaptiveOrchestrator, '_fetch_node_resources')
    def test_fetch_node_resources(self, mock_fetch_resources):
        """Test that _fetch_node_resources retrieves expected information."""
        mock_fetch_resources.return_value = {
            "cpu_usage": "30%",
            "memory_available": "2GB",
            "network_bandwidth": "15Mbps"
        }
        resource_info = self.orchestrator._fetch_node_resources(self.nodes[0])
        self.assertEqual(resource_info["cpu_usage"], "30%", "The returned CPU usage should match the mocked value.")
        self.assertEqual(resource_info["memory_available"], "2GB", "The returned memory available should match the mocked value.")
        self.assertEqual(resource_info["network_bandwidth"], "15Mbps", "The returned network bandwidth should match the mocked value.")

    @patch.object(AdaptiveOrchestrator, '_fetch_node_resources')
    @patch.object(AdaptiveOrchestrator, '_assign_tasks_adaptively')
    def test_orchestrate_nodes_loop(self, mock_assign_tasks, mock_fetch_resources):
        """Test the orchestration loop with mocked resource fetch and task assignment."""
        mock_fetch_resources.return_value = {
            "cpu_usage": "15%",
            "memory_available": "3GB",
            "network_bandwidth": "12Mbps"
        }
        mock_assign_tasks.side_effect = lambda: None
        
        self.orchestrator.start_orchestrating()
        time.sleep(3)  # Allow some time for the orchestration to run

        mock_fetch_resources.assert_called()  # Check that resources were polled
        mock_assign_tasks.assert_called()  # Check that tasks were assigned
        
        self.orchestrator.stop_orchestrating()

    @patch.object(AdaptiveOrchestrator, '_fetch_node_resources')
    @patch.object(AdaptiveOrchestrator, '_assign_tasks_adaptively')
    def test_handle_exception_during_orchestration(self, mock_assign_tasks, mock_fetch_resources):
        """Test the behavior when an exception occurs during orchestration."""
        mock_fetch_resources.side_effect = Exception("Simulated exception")
        mock_assign_tasks.side_effect = lambda: None

        self.orchestrator.start_orchestrating()
        time.sleep(3)

        # Even though an exception is raised, orchestrator should continue running
        self.assertTrue(self.orchestrator.running, "Orchestrator should still be running even after an exception.")
        
        self.orchestrator.stop_orchestrating()

    @patch.object(AdaptiveOrchestrator, '_fetch_node_resources')
    def test_assign_tasks_adaptively(self, mock_fetch_resources):
        """Test that tasks are assigned adaptively based on resource availability."""
        mock_fetch_resources.return_value = {
            "cpu_usage": "40%",
            "memory_available": "2GB",
            "network_bandwidth": "20Mbps"
        }
        
        self.orchestrator._orchestrate_nodes()  # Simulate a single orchestration cycle

        # Ensure node metrics are updated after orchestration
        self.orchestrator.node_metrics = {
            "node_1": {
                "cpu_usage": "45%",
                "memory_available": "1GB",
                "network_bandwidth": "5Mbps"
            },
            "node_2": {
                "cpu_usage": "30%",
                "memory_available": "3GB",
                "network_bandwidth": "10Mbps"
            },
            "node_3": {
                "cpu_usage": "70%",
                "memory_available": "500MB",
                "network_bandwidth": "2Mbps"
            }
        }

        self.orchestrator._assign_tasks_adaptively()

        # Check if task assignment conditions are correctly evaluated
        for node_id, metrics in self.orchestrator.node_metrics.items():
            self.assertIn("cpu_usage", metrics, "Node metrics should include 'cpu_usage'.")
            if int(metrics["cpu_usage"].strip('%')) < 50:
                self.logger.info(f"Assigning task to node {node_id} due to low CPU usage.")
            else:
                self.logger.info(f"Node {node_id} is overloaded, skipping task assignment.")

    def test_empty_node_list(self):
        """Test behavior when no nodes are provided."""
        orchestrator = AdaptiveOrchestrator(nodes=[], polling_interval=1, logger=self.logger)
        orchestrator.start_orchestrating()
        time.sleep(2)
        orchestrator.stop_orchestrating()

        # Since there are no nodes, there shouldn't be any metrics
        self.assertEqual(orchestrator.node_metrics, {}, "Node metrics should be empty when no nodes are provided.")

if __name__ == "__main__":
    unittest.main()
