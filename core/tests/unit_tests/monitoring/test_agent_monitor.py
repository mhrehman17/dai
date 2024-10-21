import unittest
from unittest.mock import patch
from typing import List
from core.monitoring.agent_monitor import AgentMonitor
from core.monitoring.agent_metrics import AgentMetrics

class TestAgentMonitor(unittest.TestCase):

    def setUp(self):
        # Setup a fresh instance of AgentMonitor for each test
        self.monitor = AgentMonitor()

    def test_initial_state(self):
        """Test the initial state of AgentMonitor."""
        # There should be no agents in the initial state
        self.assertEqual(len(self.monitor.get_all_metrics()), 0)

    @patch('random.uniform')
    def test_update_metrics_new_agent(self, mock_random):
        """Test that updating metrics for a new agent works correctly."""
        # Mock random.uniform to control the CPU and memory usage values
        mock_random.side_effect = [0.5, 0.3]  # 50% CPU, 30% memory

        # Update metrics for a new agent
        self.monitor.update_metrics('agent_1')

        # Fetch the metrics for the newly added agent
        metrics = self.monitor.get_agent_metrics('agent_1')

        # Validate the agent's metrics
        self.assertIsNotNone(metrics)
        self.assertEqual(metrics.agent_id, 'agent_1')
        self.assertEqual(metrics.cpu_usage, 50.0)
        self.assertEqual(metrics.memory_usage, 30.0)
        self.assertEqual(metrics.tasks_completed, 1)

    @patch('random.uniform')
    def test_update_metrics_existing_agent(self, mock_random):
        """Test that updating metrics for an existing agent increments the task count."""
        # Mock random.uniform to control the CPU and memory usage values
        mock_random.side_effect = [0.5, 0.3]  # First update, 50% CPU, 30% memory
        self.monitor.update_metrics('agent_1')

        mock_random.side_effect = [0.7, 0.4]  # Second update, 70% CPU, 40% memory
        self.monitor.update_metrics('agent_1')

        # Fetch the metrics after two updates
        metrics = self.monitor.get_agent_metrics('agent_1')

        # Validate that the CPU and memory usage is updated, and tasks are incremented
        self.assertEqual(metrics.cpu_usage, 70.0)
        self.assertEqual(metrics.memory_usage, 40.0)
        self.assertEqual(metrics.tasks_completed, 2)

    def test_get_metrics_non_existent_agent(self):
        """Test that getting metrics for a non-existent agent returns None."""
        metrics = self.monitor.get_agent_metrics('non_existent_agent')
        self.assertIsNone(metrics)

    @patch('random.uniform')
    def test_get_all_metrics(self, mock_random):
        """Test that metrics for all agents can be retrieved."""
        # Mock random.uniform to control the CPU and memory usage values
        mock_random.side_effect = [0.5, 0.3, 0.6, 0.4]  # CPU and memory for agent_1 and agent_2

        # Update metrics for two agents
        self.monitor.update_metrics('agent_1')
        self.monitor.update_metrics('agent_2')

        # Fetch all metrics
        all_metrics: List[AgentMetrics] = self.monitor.get_all_metrics()

        # Validate the number of agents and their details
        self.assertEqual(len(all_metrics), 2)

        # Check the details of the first agent
        agent_1_metrics = next(filter(lambda x: x.agent_id == 'agent_1', all_metrics), None)
        self.assertIsNotNone(agent_1_metrics)
        self.assertEqual(agent_1_metrics.cpu_usage, 50.0)
        self.assertEqual(agent_1_metrics.memory_usage, 30.0)
        self.assertEqual(agent_1_metrics.tasks_completed, 1)

        # Check the details of the second agent
        agent_2_metrics = next(filter(lambda x: x.agent_id == 'agent_2', all_metrics), None)
        self.assertIsNotNone(agent_2_metrics)
        self.assertEqual(agent_2_metrics.cpu_usage, 60.0)
        self.assertEqual(agent_2_metrics.memory_usage, 40.0)
        self.assertEqual(agent_2_metrics.tasks_completed, 1)

    @patch('random.uniform')
    def test_multiple_updates_for_different_agents(self, mock_random):
        """Test that multiple agents can be updated independently."""
        mock_random.side_effect = [0.5, 0.3, 0.7, 0.6]  # Random values for agent_1 and agent_2
        
        # Update metrics for agent_1
        self.monitor.update_metrics('agent_1')
        
        # Update metrics for agent_2
        self.monitor.update_metrics('agent_2')

        # Fetch individual metrics
        agent_1_metrics = self.monitor.get_agent_metrics('agent_1')
        agent_2_metrics = self.monitor.get_agent_metrics('agent_2')

        # Validate metrics for agent_1
        self.assertEqual(agent_1_metrics.cpu_usage, 50.0)
        self.assertEqual(agent_1_metrics.memory_usage, 30.0)
        self.assertEqual(agent_1_metrics.tasks_completed, 1)

        # Validate metrics for agent_2
        self.assertEqual(agent_2_metrics.cpu_usage, 70.0)
        self.assertEqual(agent_2_metrics.memory_usage, 60.0)
        self.assertEqual(agent_2_metrics.tasks_completed, 1)


if __name__ == '__main__':
    unittest.main()
