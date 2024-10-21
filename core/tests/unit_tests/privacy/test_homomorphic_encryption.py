# homomorphic_encryption.py
import unittest
from unittest.mock import patch, MagicMock
from privacy.homomorphic_encryption import HomomorphicEncryption

class TestHomomorphicEncryption(unittest.TestCase):
    def setUp(self):
        self.he = HomomorphicEncryption()

    def test_encryption_decryption(self):
        value = 42
        encrypted_value = self.he.encrypt(value)
        decrypted_value = self.he.decrypt(encrypted_value)
        self.assertEqual(decrypted_value, value)  # Verify encryption and decryption are correct

    @patch('privacy.homomorphic_encryption.aggregate_encrypted_gradients')
    def test_secure_gradient_aggregation(self, mock_aggregate):
        mock_aggregate.return_value = 100
        result = self.he.aggregate([MagicMock(), MagicMock()])
        self.assertEqual(result, 100)  # Verify secure aggregation of encrypted gradients

if __name__ == '__main__':
    unittest.main()
