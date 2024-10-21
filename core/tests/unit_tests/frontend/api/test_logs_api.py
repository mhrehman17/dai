# logs.py
import unittest
from unittest.mock import patch
from api.logs import LogsAPI
from flask import Flask

class TestLogsAPI(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.client = self.app.test_client()
        self.logs_api = LogsAPI()

    @patch('api.logs.get_logs')
    def test_log_retrieval(self, mock_get_logs):
        mock_get_logs.return_value = ({'logs': 'log_data'}, 200)
        response = self.client.get('/logs/retrieve')
        self.assertEqual(response.status_code, 200)
        self.assertIn('log_data', response.get_data(as_text=True))

    @patch('api.logs.filter_logs')
    def test_log_filtering(self, mock_filter_logs):
        mock_filter_logs.return_value = ({'filtered_logs': 'filtered_data'}, 200)
        response = self.client.get('/logs/filter', json={'component': 'component_1', 'severity': 'high'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('filtered_data', response.get_data(as_text=True))  # Ensure log filtering works by component and severity

if __name__ == '__main__':
    unittest.main()
