import unittest
from unittest.mock import patch, MagicMock
import logging
from core.communication.zk_proof_communication import ZKPCommunication  # Correct import here
from py_ecc import bn128
import secrets

class TestZKPCommunication(unittest.TestCase):

    def setUp(self):
        # Set up a logger for ZKPCommunication testing
        self.logger = logging.getLogger("test_zkp_communication")
        self.logger.setLevel(logging.INFO)
        console_handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

        # Set up ZKP Communication for testing
        self.zkp_comm = ZKPCommunication(logger=self.logger)

    def test_generate_proof(self):
        # Test generating a proof
        secret_value = 42
        proof = self.zkp_comm.generate_proof(secret=secret_value)

        # Assert proof has expected keys and types
        self.assertIn("public_key", proof)
        self.assertIn("commitment", proof)
        self.assertIn("challenge", proof)
        self.assertIsInstance(proof["public_key"], tuple)
        self.assertIsInstance(proof["commitment"], tuple)
        self.assertIsInstance(proof["challenge"], int)

        # Ensure the generated proof is on the bn128 curve
        self.assertTrue(bn128.is_on_curve(proof["public_key"], bn128.b))
        self.assertTrue(bn128.is_on_curve(proof["commitment"], bn128.b))
        self.logger.info("test_generate_proof passed")

    @patch("core.communication.zk_proof_communication.bn128.multiply")
    def test_generate_proof_mock(self, mock_multiply):
        # Mocking bn128.multiply to verify it is called with correct arguments
        secret_value = 42
        mock_multiply.return_value = (1, 2)  # Example return value on the curve (bn128 points are 2 values)

        proof = self.zkp_comm.generate_proof(secret=secret_value)
        
        # Ensure multiply was called twice (once for public key, once for commitment)
        self.assertEqual(mock_multiply.call_count, 2)
        mock_multiply.assert_any_call(bn128.G1, secret_value)
        self.logger.info("test_generate_proof_mock passed")

    def test_verify_proof_success(self):
        # Test successful verification of a generated proof
        secret_value = 42
        proof = self.zkp_comm.generate_proof(secret=secret_value)
        verification_result = self.zkp_comm.verify_proof(proof=proof, secret=secret_value)

        # Assert the proof verification succeeds
        self.assertTrue(verification_result)
        self.logger.info("test_verify_proof_success passed")

    def test_verify_proof_failure_incorrect_secret(self):
        # Test verification failure due to incorrect secret
        secret_value = 42
        wrong_secret = 24  # Different secret to simulate a failed verification
        proof = self.zkp_comm.generate_proof(secret=secret_value)
        verification_result = self.zkp_comm.verify_proof(proof=proof, secret=wrong_secret)

        # Assert the proof verification fails
        self.assertFalse(verification_result)
        self.logger.info("test_verify_proof_failure_incorrect_secret passed")

    def test_verify_proof_invalid_commitment(self):
        # Test verification failure due to invalid commitment (not on curve)
        secret_value = 42
        proof = self.zkp_comm.generate_proof(secret=secret_value)

        # Manually modify the proof commitment to an invalid value
        proof["commitment"] = (999999, 999999)  # Value that is likely not on the curve

        verification_result = self.zkp_comm.verify_proof(proof=proof, secret=secret_value)

        # Assert the proof verification fails
        self.assertFalse(verification_result)
        self.logger.info("test_verify_proof_invalid_commitment passed")

    @patch("core.communication.zk_proof_communication.secrets.randbelow")
    def test_generate_proof_with_mocked_randomness(self, mock_randbelow):
        # Mocking secrets.randbelow to verify deterministic generation of proof
        mock_randbelow.return_value = 5

        secret_value = 42
        proof = self.zkp_comm.generate_proof(secret=secret_value)

        # Assert challenge is set to mocked value
        self.assertEqual(proof["challenge"], 5)
        self.logger.info("test_generate_proof_with_mocked_randomness passed")

if __name__ == '__main__':
    unittest.main()
