# metrics.py
import unittest
from unittest.mock import patch
from api.metrics import MetricsAPI
from flask import Flask

class TestMetricsAPI(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.client = self.app.test_client()
        self.metrics_api = MetricsAPI()

    @patch('api.metrics.fetch_metrics_data')
    def test_fetch_metrics_data(self, mock_fetch_metrics):
        mock_fetch_metrics.return_value = ({'data': [1, 2, 3]}, 200)
        response = self.client.get('/metrics/fetch')
        self.assertEqual(response.status_code, 200)
        self.assertIn('data', response.get_data(as_text=True))

    @patch('api.metrics.handle_time_series_data')
    def test_time_series_handling(self, mock_handle_time_series):
        mock_handle_time_series.return_value = ({'success': True}, 200)
        response = self.client.post('/metrics/time_series', json={'series': [1, 2, 3]})
        self.assertEqual(response.status_code, 200)
        self.assertIn('success', response.get_data(as_text=True))

if __name__ == '__main__':
    unittest.main()

