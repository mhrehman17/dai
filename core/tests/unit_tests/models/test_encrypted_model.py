# encrypted_model.py
import unittest
from models.encrypted_model import EncryptedModel

class TestEncryptedModel(unittest.TestCase):
    def setUp(self):
        self.model = EncryptedModel()

    def test_homomorphic_encryption(self):
        original_weights = [0.1, 0.2, 0.3]
        encrypted_weights = self.model.encrypt_weights(original_weights)
        self.assertNotEqual(encrypted_weights, original_weights)  # Verify weights are encrypted

    def test_training_with_encrypted_gradients(self):
        encrypted_gradients = [0.5, 0.6, 0.7]  # Mock encrypted gradients
        result = self.model.train_with_encrypted_gradients(encrypted_gradients)
        self.assertTrue(result)  # Verify training succeeds with encrypted gradients

if __name__ == '__main__':
    unittest.main()

