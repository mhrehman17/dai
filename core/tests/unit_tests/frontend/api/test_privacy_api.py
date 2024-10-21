# privacy.py
import unittest
from unittest.mock import patch
from api.privacy import PrivacyAPI
from flask import Flask

class TestPrivacyAPI(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.client = self.app.test_client()
        self.privacy_api = PrivacyAPI()

    @patch('api.privacy.get_privacy_policy')
    def test_privacy_policy_settings(self, mock_get_privacy_policy):
        mock_get_privacy_policy.return_value = ({'policy': 'strict'}, 200)
        response = self.client.get('/privacy/policy')
        self.assertEqual(response.status_code, 200)
        self.assertIn('strict', response.get_data(as_text=True))

    @patch('api.privacy.modify_privacy_settings')
    def test_modify_privacy_settings(self, mock_modify_privacy):
        mock_modify_privacy.return_value = ({'message': 'Privacy settings updated'}, 200)
        response = self.client.put('/privacy/settings', json={'setting': 'relaxed'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('Privacy settings updated', response.get_data(as_text=True))

if __name__ == '__main__':
    unittest.main()
