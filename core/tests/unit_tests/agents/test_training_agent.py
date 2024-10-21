import unittest
from unittest.mock import patch
from core.agents.training_agent import TrainingAgent

class TestTrainingAgent(unittest.TestCase):

    def setUp(self):
        """
        Set up the test environment by creating an instance of TrainingAgent.
        """
        self.agent = TrainingAgent(agent_id="agent_1", description="Training agent for MNIST model")

    @patch('time.sleep', return_value=None)  # Patch time.sleep to avoid delays during tests
    @patch('random.uniform', return_value=2.5)  # Patch random.uniform to return a fixed training time
    def test_train(self, mock_sleep, mock_random):
        """
        Test the train method to ensure it updates the agent status properly.
        """
        self.assertEqual(self.agent.get_status(), "initialized")
        self.agent.train(data=[1, 2, 3, 4, 5])  # Simulate training with sample data
        self.assertEqual(self.agent.get_status(), "idle")

    @patch('random.uniform', return_value=0.85)  # Patch random.uniform to return a fixed accuracy value
    def test_evaluate(self, mock_random):
        """
        Test the evaluate method to ensure it evaluates correctly and returns a valid accuracy.
        """
        self.agent.status = "idle"  # Set status to idle before evaluating
        accuracy = self.agent.evaluate()
        self.assertEqual(self.agent.get_status(), "idle")
        self.assertAlmostEqual(accuracy, 0.85, places=2)  # Check that returned accuracy matches the mock value

    def test_get_status(self):
        """
        Test get_status method to ensure the correct status is returned.
        """
        self.assertEqual(self.agent.get_status(), "initialized")
        self.agent.status = "training"
        self.assertEqual(self.agent.get_status(), "training")
        self.agent.status = "evaluating"
        self.assertEqual(self.agent.get_status(), "evaluating")

if __name__ == '__main__':
    unittest.main()
