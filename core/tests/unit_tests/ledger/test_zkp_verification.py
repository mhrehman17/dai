import unittest
from unittest.mock import patch, MagicMock
from core.ledger.zkp_verification import ZKPVerification

class TestZKPVerification(unittest.TestCase):
    def setUp(self):
        """
        Set up an instance of ZKPVerification before each test.
        """
        self.zkp_verifier = ZKPVerification()

    @patch("core.ledger.zkp_verification.ZKPVerification.generate_proof")
    def test_generate_proof_success(self, mock_generate_proof):
        """
        Test that generate_proof successfully generates a proof.
        """
        mock_generate_proof.return_value = "Proof generated successfully"
        result = self.zkp_verifier.generate_proof("input_data")
        
        # Ensure generate_proof was called with the correct argument
        mock_generate_proof.assert_called_once_with("input_data")
        
        # Check that the returned result is correct
        self.assertEqual(result, "Proof generated successfully")

    @patch("core.ledger.zkp_verification.ZKPVerification.generate_proof")
    def test_generate_proof_failure(self, mock_generate_proof):
        """
        Test that generate_proof handles failure.
        """
        mock_generate_proof.side_effect = Exception("Proof generation failed")
        
        with self.assertRaises(Exception) as context:
            self.zkp_verifier.generate_proof("input_data")
        
        # Check that the error message matches
        self.assertTrue("Proof generation failed" in str(context.exception))

    @patch("core.ledger.zkp_verification.ZKPVerification.verify_proof")
    def test_verify_proof_success(self, mock_verify_proof):
        """
        Test that verify_proof successfully verifies a valid proof.
        """
        mock_verify_proof.return_value = True
        proof = "sample_proof"
        result = self.zkp_verifier.verify_proof(proof)

        # Ensure verify_proof was called with the correct argument
        mock_verify_proof.assert_called_once_with(proof)
        
        # Check that the proof is verified as True
        self.assertTrue(result)

    @patch("core.ledger.zkp_verification.ZKPVerification.verify_proof")
    def test_verify_proof_failure(self, mock_verify_proof):
        """
        Test that verify_proof handles invalid proofs.
        """
        mock_verify_proof.return_value = False
        proof = "invalid_proof"
        result = self.zkp_verifier.verify_proof(proof)

        # Ensure verify_proof was called with the correct argument
        mock_verify_proof.assert_called_once_with(proof)
        
        # Check that the proof is verified as False
        self.assertFalse(result)

    @patch("core.ledger.zkp_verification.ZKPVerification.validate_agent_computation")
    def test_validate_agent_computation_success(self, mock_validate_agent_computation):
        """
        Test that validate_agent_computation correctly validates agent computation.
        """
        mock_validate_agent_computation.return_value = "Agent computation validated"
        result = self.zkp_verifier.validate_agent_computation("agent_1", "computation_data")

        # Ensure validate_agent_computation was called with the correct arguments
        mock_validate_agent_computation.assert_called_once_with("agent_1", "computation_data")
        
        # Check that the result is correct
        self.assertEqual(result, "Agent computation validated")

    @patch("core.ledger.zkp_verification.ZKPVerification.validate_agent_computation")
    def test_validate_agent_computation_failure(self, mock_validate_agent_computation):
        """
        Test that validate_agent_computation handles validation failure.
        """
        mock_validate_agent_computation.side_effect = ValueError("Validation failed")
        
        with self.assertRaises(ValueError) as context:
            self.zkp_verifier.validate_agent_computation("agent_1", "invalid_computation_data")
        
        # Ensure the exception message is correct
        self.assertTrue("Validation failed" in str(context.exception))

    @patch("core.ledger.zkp_verification.ZKPVerification.validate_agent_computation")
    def test_validate_agent_computation_invalid_agent(self, mock_validate_agent_computation):
        """
        Test that validate_agent_computation handles invalid agent scenarios.
        """
        mock_validate_agent_computation.side_effect = KeyError("Invalid agent")

        with self.assertRaises(KeyError) as context:
            self.zkp_verifier.validate_agent_computation("invalid_agent", "computation_data")

        # Ensure the exception message matches
        self.assertTrue("Invalid agent" in str(context.exception))

    def tearDown(self):
        """
        Clean up after each test.
        """
        self.zkp_verifier = None

if __name__ == "__main__":
    unittest.main()
