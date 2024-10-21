import unittest
from unittest.mock import patch
from flask import Flask
from flask.testing import FlaskClient
from api.endpoints.agents import AgentsAPI
import pytest

# Integration tests for Agents API and Core Agents Logic
@pytest.fixture
def app():
    app = Flask(__name__)
    app.register_blueprint(AgentsAPI, url_prefix='/agents')
    return app

@pytest.fixture
def client(app) -> FlaskClient:
    return app.test_client()

@patch('api.endpoints.agents.register_agent')
def test_register_agent_success(mock_register_agent, client):
    # Simulate successful agent registration
    mock_register_agent.return_value = {'message': 'Agent registered successfully'}, 201
    response = client.post('/agents/register', json={'agent_name': 'Test Agent'})
    assert response.status_code == 201
    assert 'Agent registered successfully' in response.get_data(as_text=True)

@patch('api.endpoints.agents.register_agent')
def test_register_agent_failure(mock_register_agent, client):
    # Simulate failed agent registration (e.g., duplicate agent)
    mock_register_agent.side_effect = ValueError('Agent already exists')
    response = client.post('/agents/register', json={'agent_name': 'Test Agent'})
    assert response.status_code == 400
    assert 'Agent already exists' in response.get_data(as_text=True)

@patch('api.endpoints.agents.update_agent')
def test_update_agent_success(mock_update_agent, client):
    # Simulate successful agent update
    mock_update_agent.return_value = {'message': 'Agent updated successfully'}, 200
    response = client.put('/agents/update', json={'agent_id': 1, 'new_status': 'active'})
    assert response.status_code == 200
    assert 'Agent updated successfully' in response.get_data(as_text=True)

@patch('api.endpoints.agents.update_agent')
def test_update_agent_failure(mock_update_agent, client):
    # Simulate update failure due to nonexistent agent
    mock_update_agent.side_effect = KeyError('Agent not found')
    response = client.put('/agents/update', json={'agent_id': 999, 'new_status': 'active'})
    assert response.status_code == 404
    assert 'Agent not found' in response.get_data(as_text=True)

@patch('api.endpoints.agents.remove_agent')
def test_remove_agent_success(mock_remove_agent, client):
    # Simulate successful agent removal
    mock_remove_agent.return_value = {'message': 'Agent removed successfully'}, 200
    response = client.delete('/agents/remove', json={'agent_id': 1})
    assert response.status_code == 200
    assert 'Agent removed successfully' in response.get_data(as_text=True)

@patch('api.endpoints.agents.remove_agent')
def test_remove_agent_failure(mock_remove_agent, client):
    # Simulate agent removal failure (e.g., agent does not exist)
    mock_remove_agent.side_effect = KeyError('Agent not found')
    response = client.delete('/agents/remove', json={'agent_id': 999})
    assert response.status_code == 404
    assert 'Agent not found' in response.get_data(as_text=True)

if __name__ == '__main__':
    pytest.main()
