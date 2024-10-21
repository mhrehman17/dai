# agents.py
import unittest
from unittest.mock import patch, MagicMock
from api.agents import AgentsAPI
from flask import Flask

class TestAgentsAPI(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.client = self.app.test_client()
        self.agents_api = AgentsAPI()

    @patch('api.agents.register_agent')
    def test_register_agent(self, mock_register_agent):
        mock_register_agent.return_value = ({'message': 'Agent registered'}, 201)
        response = self.client.post('/agents/register', json={'name': 'agent_1'})
        self.assertEqual(response.status_code, 201)
        self.assertIn('Agent registered', response.get_data(as_text=True))

    @patch('api.agents.update_agent')
    def test_update_agent(self, mock_update_agent):
        mock_update_agent.return_value = ({'message': 'Agent updated'}, 200)
        response = self.client.put('/agents/update', json={'agent_id': '1', 'status': 'active'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('Agent updated', response.get_data(as_text=True))

    @patch('api.agents.remove_agent')
    def test_remove_agent(self, mock_remove_agent):
        mock_remove_agent.return_value = ({'message': 'Agent removed'}, 200)
        response = self.client.delete('/agents/remove', json={'agent_id': '1'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('Agent removed', response.get_data(as_text=True))

if __name__ == '__main__':
    unittest.main()