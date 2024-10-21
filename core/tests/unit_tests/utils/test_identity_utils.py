import unittest
from core.utils.identity_utils import IdentityUtils
from unittest.mock import patch, MagicMock

class TestIdentityUtils(unittest.TestCase):
    def setUp(self):
        # Set up an instance of the IdentityUtils before each test
        self.identity_utils = IdentityUtils()

    @patch("core.utils.identity_utils.IdentityUtils.verify_identity")
    def test_verify_identity(self, mock_verify_identity):
        # Test verifying identity using tokens
        mock_verify_identity.return_value = True
        token = "valid_token"
        result = self.identity_utils.verify_identity(token)
        mock_verify_identity.assert_called_once_with(token)
        self.assertTrue(result)

    @patch("core.utils.identity_utils.IdentityUtils.generate_token")
    def test_generate_token(self, mock_generate_token):
        # Test generating a token for an agent
        mock_generate_token.return_value = "generated_token"
        agent_id = "agent_1"
        result = self.identity_utils.generate_token(agent_id)
        mock_generate_token.assert_called_once_with(agent_id)
        self.assertEqual(result, "generated_token")

    @patch("core.utils.identity_utils.IdentityUtils.revoke_token")
    def test_revoke_token(self, mock_revoke_token):
        # Test revoking a token
        mock_revoke_token.return_value = "Token revoked"
        token = "expired_token"
        result = self.identity_utils.revoke_token(token)
        mock_revoke_token.assert_called_once_with(token)
        self.assertEqual(result, "Token revoked")

    def tearDown(self):
        # Clean up after each test
        self.identity_utils = None

if __name__ == "__main__":
    unittest.main()
