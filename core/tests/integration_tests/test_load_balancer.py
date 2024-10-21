import unittest
from core.orchestrator.decentralized_orchestrator import DecentralizedOrchestrator
from core.orchestrator.load_balancer import LoadBalancer
from core.agents.training_agent import TrainingAgent

class TestOrchestratorLoadBalancerIntegration(unittest.TestCase):
    def setUp(self):
        """
        Set up the test environment for Orchestrator and Load Balancer integration tests.
        """
        self.orchestrator = DecentralizedOrchestrator()
        self.load_balancer = LoadBalancer()

        # Create agents
        self.agent_1 = TrainingAgent(agent_id="agent_1", description="Training Agent 1")
        self.agent_2 = TrainingAgent(agent_id="agent_2", description="Training Agent 2")
        self.agent_3 = TrainingAgent(agent_id="agent_3", description="Training Agent 3")

        # Register agents with load balancer
        self.load_balancer.register_agent(self.agent_1)
        self.load_balancer.register_agent(self.agent_2)
        self.load_balancer.register_agent(self.agent_3)

    def test_orchestrator_task_allocation(self):
        """
        Test if the orchestrator can allocate tasks to agents using the load balancer.
        """
        # Register agents with orchestrator
        self.orchestrator.register_agent(self.agent_1)
        self.orchestrator.register_agent(self.agent_2)
        self.orchestrator.register_agent(self.agent_3)

        # Use load balancer to allocate tasks
        allocated_agent_id = self.load_balancer.allocate_task("Training Task 1")
        self.assertIn(allocated_agent_id, ["agent_1", "agent_2", "agent_3"], "Task should be allocated to one of the registered agents.")

    def test_task_assignment_and_status(self):
        """
        Test if the orchestrator can assign tasks and check their status using registered agents.
        """
        # Register agents with orchestrator
        self.orchestrator.register_agent(self.agent_1)
        self.orchestrator.register_agent(self.agent_2)
        self.orchestrator.register_agent(self.agent_3)

        # Assign a task using orchestrator
        self.orchestrator.start_task(task_id="task_1", agent_ids=["agent_1", "agent_2"], description="Federated Training Task")

        # Check task status
        task_status = self.orchestrator.get_task_status("task_1")
        self.assertIsNotNone(task_status, "Task status should not be None.")
        self.assertEqual(task_status["status"], "completed", "Task status should be 'completed'.")

    def test_orchestrator_and_load_balancer_interaction(self):
        """
        Test if the orchestrator can interact with the load balancer to allocate resources dynamically.
        """
        # Register agents with orchestrator
        self.orchestrator.register_agent(self.agent_1)
        self.orchestrator.register_agent(self.agent_2)
        self.orchestrator.register_agent(self.agent_3)

        # Allocate a task dynamically using the load balancer
        allocated_agent_id = self.load_balancer.allocate_task("Dynamic Training Task")
        self.assertIn(allocated_agent_id, ["agent_1", "agent_2", "agent_3"], "Allocated agent must be one of the registered agents.")

        # Start a task with the allocated agent using the orchestrator
        self.orchestrator.start_task(task_id="task_dynamic", agent_ids=[allocated_agent_id], description="Dynamic Allocation Task")
        task_status = self.orchestrator.get_task_status("task_dynamic")
        self.assertIsNotNone(task_status, "Task status should not be None.")
        self.assertEqual(task_status["status"], "completed", "Task should be marked as 'completed'.")

if __name__ == "__main__":
    unittest.main()