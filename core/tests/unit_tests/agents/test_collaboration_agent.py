import unittest
from unittest.mock import patch, MagicMock
from core.agents.collaboration_agent import CollaborationAgent
from core.agents.training_agent import TrainingAgent

class TestCollaborationAgent(unittest.TestCase):

    def setUp(self):
        # Create instances of CollaborationAgent for testing
        self.agent_1 = CollaborationAgent(agent_id="agent_1", description="Collaboration agent 1")
        self.agent_2 = CollaborationAgent(agent_id="agent_2", description="Collaboration agent 2")
        self.agent_3 = CollaborationAgent(agent_id="agent_3", description="Collaboration agent 3")

    def test_add_peer(self):
        # Test adding peers to the collaboration network
        self.agent_1.add_peer(self.agent_2)
        self.agent_1.add_peer(self.agent_3)

        self.assertEqual(len(self.agent_1.peers), 2)
        self.assertIn(self.agent_2, self.agent_1.peers)
        self.assertIn(self.agent_3, self.agent_1.peers)

    def test_add_duplicate_peer(self):
        # Test adding the same peer twice
        self.agent_1.add_peer(self.agent_2)
        self.agent_1.add_peer(self.agent_2)

        self.assertEqual(len(self.agent_1.peers), 1)  # Should only have 1 unique peer

    def test_remove_peer(self):
        # Test removing a peer from the collaboration network
        self.agent_1.add_peer(self.agent_2)
        self.agent_1.add_peer(self.agent_3)
        self.agent_1.remove_peer(self.agent_2.agent_id)

        self.assertEqual(len(self.agent_1.peers), 1)
        self.assertNotIn(self.agent_2, self.agent_1.peers)
        self.assertIn(self.agent_3, self.agent_1.peers)

    def test_remove_nonexistent_peer(self):
        # Test removing a peer that does not exist
        self.agent_1.add_peer(self.agent_2)
        self.agent_1.remove_peer("nonexistent_agent")

        self.assertEqual(len(self.agent_1.peers), 1)
        self.assertIn(self.agent_2, self.agent_1.peers)

    @patch('time.sleep', return_value=None)  # To skip the sleep in testing
    def test_collaborate_no_peers(self, mock_sleep):
        # Test collaborate method with no peers
        with patch('builtins.print') as mock_print:
            self.agent_1.collaborate()
            mock_print.assert_any_call("Agent agent_1 has no peers to collaborate with.")

    @patch('time.sleep', return_value=None)  # To skip the sleep in testing
    def test_collaborate_with_peers(self, mock_sleep):
        # Test collaborate method with peers
        self.agent_1.add_peer(self.agent_2)
        self.agent_1.add_peer(self.agent_3)

        with patch('builtins.print') as mock_print:
            self.agent_1.collaborate()
            mock_print.assert_any_call("Agent agent_1 is collaborating with peers...")
            mock_print.assert_any_call("Agent agent_1 is sending updates to peer agent_2.")
            mock_print.assert_any_call("Agent agent_1 is sending updates to peer agent_3.")
            mock_print.assert_any_call("Agent agent_1 completed collaboration with peers.")

    @patch('time.sleep', return_value=None)  # To skip the sleep in testing
    def test_train_with_collaboration(self, mock_sleep):
        # Test the overridden train method which includes collaboration after training
        self.agent_1.add_peer(self.agent_2)
        
        with patch('builtins.print') as mock_print:
            self.agent_1.train()
            # Check that training started
            mock_print.assert_any_call("Agent agent_1 is starting training...")
            # Use a partial match for the training complete message
            calls = [call[0][0] for call in mock_print.call_args_list]
            training_complete_message = next((msg for msg in calls if "Training complete for Agent agent_1 in" in msg), None)
            self.assertIsNotNone(training_complete_message, "Training complete message was not printed.")
            # Check that collaboration started
            mock_print.assert_any_call("Agent agent_1 is collaborating with peers...")

    def test_get_status(self):
        # Test getting the agent's current status
        self.assertEqual(self.agent_1.get_status(), "initialized")
        self.agent_1.status = "training"
        self.assertEqual(self.agent_1.get_status(), "training")

if __name__ == '__main__':
    unittest.main()
