import unittest
from unittest.mock import patch
from flask import Flask
from flask.testing import FlaskClient
from api.endpoints.orchestrator import OrchestratorAPI
import pytest

# Integration tests for Orchestrator API and Core Orchestrator Logic

@pytest.fixture
def app():
    app = Flask(__name__)
    app.register_blueprint(OrchestratorAPI, url_prefix='/orchestrator')
    return app

@pytest.fixture
def client(app) -> FlaskClient:
    return app.test_client()

@patch('api.endpoints.orchestrator.assign_task')
def test_assign_task_success(mock_assign_task, client):
    # Simulate successful task assignment
    mock_assign_task.return_value = {'message': 'Task assigned successfully'}, 200
    response = client.post('/orchestrator/assign_task', json={'task_id': 'task_1', 'agent_id': 'agent_1'})
    assert response.status_code == 200
    assert 'Task assigned successfully' in response.get_data(as_text=True)

@patch('api.endpoints.orchestrator.assign_task')
def test_assign_task_failure(mock_assign_task, client):
    # Simulate failed task assignment (e.g., invalid agent ID)
    mock_assign_task.side_effect = ValueError('Agent not found')
    response = client.post('/orchestrator/assign_task', json={'task_id': 'task_1', 'agent_id': 'invalid_agent'})
    assert response.status_code == 400
    assert 'Agent not found' in response.get_data(as_text=True)

@patch('api.endpoints.orchestrator.get_health_status')
def test_get_health_status_success(mock_get_health_status, client):
    # Simulate successful health status retrieval
    mock_get_health_status.return_value = {'status': 'healthy', 'agents': 5}, 200
    response = client.get('/orchestrator/health_status')
    assert response.status_code == 200
    assert 'healthy' in response.get_data(as_text=True)
    assert 'agents' in response.get_data(as_text=True)

@patch('api.endpoints.orchestrator.get_health_status')
def test_get_health_status_failure(mock_get_health_status, client):
    # Simulate failure in retrieving health status (e.g., orchestrator not available)
    mock_get_health_status.side_effect = RuntimeError('Orchestrator unavailable')
    response = client.get('/orchestrator/health_status')
    assert response.status_code == 503
    assert 'Orchestrator unavailable' in response.get_data(as_text=True)

@patch('api.endpoints.orchestrator.rebalance_tasks')
def test_rebalance_tasks_success(mock_rebalance_tasks, client):
    # Simulate successful task rebalancing
    mock_rebalance_tasks.return_value = {'message': 'Tasks rebalanced successfully'}, 200
    response = client.post('/orchestrator/rebalance_tasks')
    assert response.status_code == 200
    assert 'Tasks rebalanced successfully' in response.get_data(as_text=True)

@patch('api.endpoints.orchestrator.rebalance_tasks')
def test_rebalance_tasks_failure(mock_rebalance_tasks, client):
    # Simulate failure in rebalancing tasks (e.g., insufficient resources)
    mock_rebalance_tasks.side_effect = RuntimeError('Insufficient resources for rebalancing')
    response = client.post('/orchestrator/rebalance_tasks')
    assert response.status_code == 500
    assert 'Insufficient resources for rebalancing' in response.get_data(as_text=True)

if __name__ == '__main__':
    pytest.main()
