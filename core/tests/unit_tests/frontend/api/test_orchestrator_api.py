# orchestrator.py
import unittest
from unittest.mock import patch
from api.orchestrator import OrchestratorAPI
from flask import Flask

class TestOrchestratorAPI(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.client = self.app.test_client()
        self.orchestrator_api = OrchestratorAPI()

    @patch('api.orchestrator.assign_task')
    def test_assign_task(self, mock_assign_task):
        mock_assign_task.return_value = ({'message': 'Task assigned'}, 200)
        response = self.client.post('/orchestrator/assign_task', json={'task_id': 'task_1'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('Task assigned', response.get_data(as_text=True))

    @patch('api.orchestrator.get_health_status')
    def test_get_health_status(self, mock_get_health_status):
        mock_get_health_status.return_value = ({'status': 'healthy'}, 200)
        response = self.client.get('/orchestrator/health_status')
        self.assertEqual(response.status_code, 200)
        self.assertIn('healthy', response.get_data(as_text=True))

if __name__ == '__main__':
    unittest.main()
