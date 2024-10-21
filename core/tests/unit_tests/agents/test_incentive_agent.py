import unittest
from unittest.mock import patch, MagicMock
from core.agents.incentive_agent import IncentiveAgent
from core.agents.collaboration_agent import CollaborationAgent

class TestIncentiveAgent(unittest.TestCase):
    
    def setUp(self):
        # Create an IncentiveAgent instance
        self.agent_1 = IncentiveAgent(agent_id="agent_1", description="Incentive agent 1 for rewarding contributions")
        # Create additional agents to act as peers
        self.agent_2 = IncentiveAgent(agent_id="agent_2", description="Incentive agent 2 for rewarding contributions")
        self.agent_3 = IncentiveAgent(agent_id="agent_3", description="Incentive agent 3 for rewarding contributions")

    def test_add_peer(self):
        # Test adding peers and initializing their reputation
        self.agent_1.add_peer(self.agent_2)
        self.agent_1.add_peer(self.agent_3)

        # Assert peers have been added
        self.assertIn(self.agent_2.agent_id, self.agent_1.reputation_scores)
        self.assertIn(self.agent_3.agent_id, self.agent_1.reputation_scores)
        
        # Assert initial reputation score
        self.assertEqual(self.agent_1.reputation_scores[self.agent_2.agent_id], 1.0)
        self.assertEqual(self.agent_1.reputation_scores[self.agent_3.agent_id], 1.0)

    def test_reward_peer(self):
        # Test rewarding a peer
        self.agent_1.add_peer(self.agent_2)
        self.agent_1.reward_peer(self.agent_2.agent_id, 0.5)

        # Assert the reputation score is incremented correctly
        self.assertEqual(self.agent_1.reputation_scores[self.agent_2.agent_id], 1.5)

    def test_reward_peer_not_found(self):
        # Test rewarding a peer that hasn't been added
        with patch('builtins.print') as mocked_print:
            self.agent_1.reward_peer("non_existent_peer", 0.5)
            mocked_print.assert_called_once_with("Agent agent_1 could not find peer non_existent_peer to reward.")

    def test_penalize_peer(self):
        # Test penalizing a peer
        self.agent_1.add_peer(self.agent_2)
        self.agent_1.penalize_peer(self.agent_2.agent_id, 0.2)

        # Assert the reputation score is decremented correctly, but not below 0
        self.assertEqual(self.agent_1.reputation_scores[self.agent_2.agent_id], 0.8)

    def test_penalize_peer_not_found(self):
        # Test penalizing a peer that hasn't been added
        with patch('builtins.print') as mocked_print:
            self.agent_1.penalize_peer("non_existent_peer", 0.2)
            mocked_print.assert_called_once_with("Agent agent_1 could not find peer non_existent_peer to penalize.")

    @patch('core.agents.incentive_agent.random.choice', return_value=True)
    @patch('core.agents.incentive_agent.random.uniform', return_value=0.3)
    def test_collaborate_reward_success(self, mock_random_uniform, mock_random_choice):
        # Test successful collaboration where peers are rewarded
        self.agent_1.add_peer(self.agent_2)
        self.agent_1.collaborate()

        # Assert the peer was rewarded correctly
        self.assertEqual(self.agent_1.reputation_scores[self.agent_2.agent_id], 1.3)

    @patch('core.agents.incentive_agent.random.choice', return_value=False)
    @patch('core.agents.incentive_agent.random.uniform', return_value=0.1)
    def test_collaborate_penalize_failure(self, mock_random_uniform, mock_random_choice):
        # Test failed collaboration where peers are penalized
        self.agent_1.add_peer(self.agent_2)
        self.agent_1.collaborate()

        # Assert the peer was penalized correctly
        self.assertEqual(self.agent_1.reputation_scores[self.agent_2.agent_id], 0.9)

if __name__ == '__main__':
    unittest.main()
