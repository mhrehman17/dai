import unittest
from unittest.mock import MagicMock
import logging
from core.communication.access_policy import AccessPolicy  # Assuming the code is stored in core/utils/access_policy.py

class TestAccessPolicy(unittest.TestCase):

    def setUp(self):
        # Mock logger to verify logging outputs
        self.mock_logger = MagicMock(spec=logging.Logger)
        self.access_policy = AccessPolicy(logger=self.mock_logger)

    def test_define_policy(self):
        # Define an access policy
        self.access_policy.define_policy(agent_id="agent_1", allowed_peers=["agent_2", "agent_3"])

        # Check if the policy is correctly added
        self.assertIn("agent_1", self.access_policy.access_policies)
        self.assertListEqual(self.access_policy.access_policies["agent_1"], ["agent_2", "agent_3"])

        # Check if correct info logging happened
        self.mock_logger.info.assert_called_with("Access policy defined for agent 'agent_1': Allowed peers: ['agent_2', 'agent_3']")

    def test_can_communicate_allowed(self):
        # Define an access policy and check communication permissions
        self.access_policy.define_policy(agent_id="agent_1", allowed_peers=["agent_2", "agent_3"])
        can_communicate = self.access_policy.can_communicate(agent_id="agent_1", target_peer_id="agent_2")

        # Should allow communication
        self.assertTrue(can_communicate)
        self.mock_logger.info.assert_called_with("Communication allowed between agent 'agent_1' and target peer 'agent_2'")

    def test_can_communicate_denied(self):
        # Define an access policy and check denied communication
        self.access_policy.define_policy(agent_id="agent_1", allowed_peers=["agent_2", "agent_3"])
        can_communicate = self.access_policy.can_communicate(agent_id="agent_1", target_peer_id="agent_4")

        # Should not allow communication
        self.assertFalse(can_communicate)
        self.mock_logger.info.assert_called_with("Communication denied between agent 'agent_1' and target peer 'agent_4'")

    def test_revoke_policy_existing_agent(self):
        # Define and revoke an access policy
        self.access_policy.define_policy(agent_id="agent_1", allowed_peers=["agent_2", "agent_3"])
        self.access_policy.revoke_policy(agent_id="agent_1")

        # Verify the policy is revoked
        self.assertNotIn("agent_1", self.access_policy.access_policies)
        self.mock_logger.info.assert_called_with("Access policy revoked for agent 'agent_1'")

    def test_revoke_policy_nonexistent_agent(self):
        # Attempt to revoke a policy for a non-existent agent
        self.access_policy.revoke_policy(agent_id="agent_unknown")

        # Verify logging to indicate no action was needed
        self.mock_logger.info.assert_called_with("No access policy found for agent 'agent_unknown', nothing to revoke.")

    def test_update_policy_existing_agent(self):
        # Define and then update an access policy
        self.access_policy.define_policy(agent_id="agent_1", allowed_peers=["agent_2"])
        self.access_policy.update_policy(agent_id="agent_1", allowed_peers=["agent_3", "agent_4"])

        # Verify the policy is updated
        self.assertListEqual(self.access_policy.access_policies["agent_1"], ["agent_3", "agent_4"])
        self.mock_logger.info.assert_called_with("Access policy updated for agent 'agent_1': New allowed peers: ['agent_3', 'agent_4']")

    def test_update_policy_nonexistent_agent(self):
        # Attempt to update a policy for a non-existent agent, which should create a new policy
        self.access_policy.update_policy(agent_id="agent_1", allowed_peers=["agent_3", "agent_4"])

        # Verify the policy is added
        self.assertIn("agent_1", self.access_policy.access_policies)
        self.assertListEqual(self.access_policy.access_policies["agent_1"], ["agent_3", "agent_4"])
        self.mock_logger.info.assert_called_with("Access policy did not exist for agent 'agent_1', a new policy has been defined.")

    def test_define_update_revoke_policy_flow(self):
        # Test the complete flow of defining, updating, and revoking policies
        self.access_policy.define_policy(agent_id="agent_1", allowed_peers=["agent_2"])
        self.access_policy.update_policy(agent_id="agent_1", allowed_peers=["agent_2", "agent_3"])
        self.access_policy.revoke_policy(agent_id="agent_1")

        # Check that the policy was defined and then updated
        self.mock_logger.info.assert_any_call("Access policy defined for agent 'agent_1': Allowed peers: ['agent_2']")
        self.mock_logger.info.assert_any_call("Access policy updated for agent 'agent_1': New allowed peers: ['agent_2', 'agent_3']")
        self.mock_logger.info.assert_any_call("Access policy revoked for agent 'agent_1'")

if __name__ == "__main__":
    unittest.main()
