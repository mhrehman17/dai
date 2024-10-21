import unittest
from unittest.mock import MagicMock, patch
from core.agents.training_agent import TrainingAgent
from core.agents.identity_management import IdentityManagement
from core.orchestrator.load_balancer import LoadBalancer
from core.orchestrator.decentralized_orchestrator import DecentralizedOrchestrator  # Assuming the original code is saved as decentralized_orchestrator.py

class TestDecentralizedOrchestrator(unittest.TestCase):

    def setUp(self):
        """Set up common test assets."""
        self.identity_manager = MagicMock(spec=IdentityManagement)
        self.load_balancer = MagicMock(spec=LoadBalancer)
        self.orchestrator = DecentralizedOrchestrator()
        self.orchestrator.identity_manager = self.identity_manager
        self.orchestrator.load_balancer = self.load_balancer

    @patch.object(IdentityManagement, 'generate_agent_id', return_value='agent_1')
    def test_register_agent(self, mock_generate_agent_id):
        """Test registering an agent."""
        agent = MagicMock(spec=TrainingAgent)
        self.identity_manager.generate_agent_id.return_value = 'agent_1'
        agent_id = self.orchestrator.register_agent(agent)
        
        self.assertIn(agent_id, self.orchestrator.agents, "Agent should be registered in orchestrator.")
        self.load_balancer.register_agent.assert_called_once_with(agent)
        mock_generate_agent_id.assert_called_once()
        self.assertEqual(agent_id, 'agent_1', "Agent ID should match the mocked value.")

    def test_unregister_agent(self):
        """Test unregistering an agent."""
        agent = MagicMock(spec=TrainingAgent)
        self.orchestrator.agents['agent_1'] = agent
        self.orchestrator.unregister_agent('agent_1')

        self.assertNotIn('agent_1', self.orchestrator.agents, "Agent should be unregistered from orchestrator.")
        self.load_balancer.unregister_agent.assert_called_once_with('agent_1')

    def test_unregister_nonexistent_agent(self):
        """Test attempting to unregister a nonexistent agent."""
        with patch('builtins.print') as mock_print:
            self.orchestrator.unregister_agent('agent_999')
            mock_print.assert_called_once_with("Agent agent_999 not found for unregistration.")

    def test_start_task_with_registered_agents(self):
        """Test starting a task with registered agents."""
        agent_1 = MagicMock(spec=TrainingAgent)
        agent_2 = MagicMock(spec=TrainingAgent)
        self.orchestrator.agents['agent_1'] = agent_1
        self.orchestrator.agents['agent_2'] = agent_2

        with patch('builtins.print') as mock_print:
            self.orchestrator.start_task(task_id='task_1', agent_ids=['agent_1', 'agent_2'], description='Test Task')
            agent_1.train.assert_called_once()
            agent_2.train.assert_called_once()
            self.assertIn('task_1', self.orchestrator.tasks, "Task should be stored in orchestrator's tasks.")
            self.assertEqual(self.orchestrator.tasks['task_1']['status'], 'completed', "Task status should be 'completed'.")
            mock_print.assert_any_call("Orchestrator is assigning task 'task_1' to agent agent_1...")
            mock_print.assert_any_call("Orchestrator is assigning task 'task_1' to agent agent_2...")

    def test_start_task_with_non_registered_agent(self):
        """Test starting a task with a non-registered agent."""
        agent_1 = MagicMock(spec=TrainingAgent)
        self.orchestrator.agents['agent_1'] = agent_1

        with patch('builtins.print') as mock_print:
            self.orchestrator.start_task(task_id='task_1', agent_ids=['agent_1', 'agent_999'], description='Test Task')
            mock_print.assert_called_once_with("One or more agents specified for task task_1 are not registered.")
            self.assertNotIn('task_1', self.orchestrator.tasks, "Task should not be stored since one or more agents are not registered.")

    def test_get_task_status(self):
        """Test retrieving the status of a specific task."""
        self.orchestrator.tasks['task_1'] = {
            "description": "Test Task",
            "agents": ["agent_1"],
            "status": "completed"
        }
        task_status = self.orchestrator.get_task_status('task_1')
        self.assertEqual(task_status['status'], 'completed', "Task status should be 'completed'.")

        # Test non-existent task
        task_status = self.orchestrator.get_task_status('task_999')
        self.assertEqual(task_status, {}, "Non-existent task should return an empty dictionary.")

    def test_list_agents(self):
        """Test listing all registered agents."""
        agent_1 = MagicMock(spec=TrainingAgent)
        agent_2 = MagicMock(spec=TrainingAgent)
        self.orchestrator.agents['agent_1'] = agent_1
        self.orchestrator.agents['agent_2'] = agent_2

        agent_list = self.orchestrator.list_agents()
        self.assertListEqual(agent_list, ['agent_1', 'agent_2'], "List of agents should match the registered agents.")

if __name__ == "__main__":
    unittest.main()
