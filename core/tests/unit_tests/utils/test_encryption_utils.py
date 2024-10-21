# encryption_utils.py
import unittest
from utilities.encryption_utils import EncryptionUtils

class TestEncryptionUtils(unittest.TestCase):
    def setUp(self):
        self.encryption_utils = EncryptionUtils()

    def test_symmetric_encryption(self):
        original_data = 'secret_data'
        encrypted_data = self.encryption_utils.symmetric_encrypt(original_data)
        decrypted_data = self.encryption_utils.symmetric_decrypt(encrypted_data)
        self.assertEqual(decrypted_data, original_data)  # Verify symmetric encryption and decryption

    def test_asymmetric_encryption(self):
        original_data = 'secret_data'
        public_key, private_key = self.encryption_utils.generate_asymmetric_keys()
        encrypted_data = self.encryption_utils.asymmetric_encrypt(original_data, public_key)
        decrypted_data = self.encryption_utils.asymmetric_decrypt(encrypted_data, private_key)
        self.assertEqual(decrypted_data, original_data)  # Verify asymmetric encryption and decryption

if __name__ == '__main__':
    unittest.main()
